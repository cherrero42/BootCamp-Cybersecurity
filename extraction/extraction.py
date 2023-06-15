#!/usr/bin/env python
# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    extraction.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cherrero <cherrero@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/05/19 11:09:21 by cherrero          #+#    #+#              #
#    Updated: 2023/06/15 13:22:43 by cherrero         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import sys
import argparse
import datetime
import time
import pytsk3
from tabulate import tabulate
import psutil
from tqdm import tqdm
import pandas as pd
import subprocess
import re
import curses

'''magic numbers for file types'''
magics = {
    "jpg" : [b"\xff\xd8\xff\xe0\x00\x10\x4a\x46", b"\xff\xd9"],
    "png" : [b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a", b"\x49\x45\x4e\x44\xae\x42\x60\x82"],
    "pdf" : [b"\x25\x50\x44\x46", b"\x25\x25\x45\x4f\x46"],
    "gif" : [b"\x47\x49\x46\x38", b"\x00\x3b"],
    "xml" : [b"\x50\x4b\x03\x04\x14\x00\x06\x00", b"\x50\x4b\x05\x06"],
}

good_recovered_files = []
recoverable = {}
selected_files = {}
disk = ""

'''path to analyzeMFT module'''
analyzeMFT_path = "./analyzeMFT/analyzeMFT.py"

'''path to MFT file'''
mft_file_path = "./analyzeMFT/mft_tmp"

'''path to MFT parsed file'''
mft_parse_file_path = "./analyzeMFT/mft_tmp.csv"

def ft_create_image_from_disk(disk_path, image_path):
    '''Create image from disk'''
    disk = rf"\\.\\{disk_path}"
    img_info = pytsk3.Img_Info(disk)
    # Open the output file in write-binary mode
    with open(image_path, "wb") as output_file:
        # Read and write the contents of the disk to the output file
        offset = 0
        chunk_size = 1024 * 1024  # 1MB chunk size (adjust as needed)
        while offset < img_info.get_size():
            data = img_info.read(offset, chunk_size)
            output_file.write(data)
            offset += chunk_size
    print(f"Image {image_path} created successfully")

def ft_read_disk(disk):
    '''Read disk'''
    # Open the image file and create an image object
    image = pytsk3.Img_Info(disk)
    # Open the partition table
    try:
        partitionTable = pytsk3.Volume_Info(image)
    except Exception as error:
        print(error)
        exit(1)
    # Open the file system and retrieve the root directory
    try:
        fileSystemObject = pytsk3.FS_Info(image, offset=partitionTable[0].start*512)
    except Exception as error:
        print(error)
        exit(1)
    return fileSystemObject

def ft_parse_MFT(mft_file_path):
    '''Parse MFT file'''
    command = ["python3", analyzeMFT_path, "-f", mft_file_path,  "-o", mft_parse_file_path]
    subprocess.run(command)

def ft_check_MFT(mft_parse_file_path):
    ''' Check & read MFT file'''
    df = pd.read_csv(mft_parse_file_path, encoding="latin-1")

    for index, row in df.iterrows():
        good_value = row['Good']
        record_type = row['Record type']
        modif_date = row['Std Info Access date']
        filename1 = row['Filename #1']
        active_value = row['Active']
        if good_value == 'Good' and record_type == 'File' and active_value == "Inactive":
            '''Recoverable files'''
            if "Zone.Identifier" not in filename1:
                good_recovered_files.append([filename1, modif_date])

def ft_extract_MFT(file):
    '''Extract MFT file'''
    content = file.read_random(0, file.info.meta.size)
    with open(mft_file_path, 'wb') as output:
        output.write(content)

def ft_search_deleted_files(disk_path):
    '''Search deleted files'''
    disk = rf"\\.\\{disk_path}"
    try:
        img_info = pytsk3.Img_Info(disk)
        fs_info = pytsk3.FS_Info(img_info)
        root_dir = fs_info.open_dir(path="/")
        mft_file = fs_info.open("/$MFT")
    except:
        print("Disk not found")
        sys.exit()
    ft_extract_MFT(mft_file)
    ft_parse_MFT(mft_file_path)
    ft_check_MFT(mft_parse_file_path)

def ft_deep_search(disk_path):
    '''Deep search for deleted files (with magik) in whole disk'''
    total = None
    for disk in psutil.disk_partitions():
        if disk_path in disk.device or disk_path in disk.mountpoint:
            total = psutil.disk_usage(disk.mountpoint).total
    if total is None:
        print("Error: Disk not found")
        sys.exit()
    size = 512
    blocks = total/size
    count = 0
    offset = 0
    with tqdm(total=blocks, unit='block') as progress_bar:
        try:
            d = open(f"\\\\.\\\\{disk_path}", "rb")
        except:
            print("Disk cannot be read, format must be: \\\\.\\\\D:")
            sys.exit()
        else:
            bytes = d.read(size)
            progress_bar.update(1)
            try:
                while bytes:
                    for key, value in magics.items():
                        found = bytes.find(value[0])
                        if found >= 0:
                            drec = True
                            if not os.path.exists(".\\Recovered_deep"):
                                os.makedirs(".\\Recovered_deep")     
                            with open(f".\\Recovered_deep\\{str(count)}.{key}", "wb") as f:
                                f.write(bytes[found:])
                                while drec is True:
                                    bytes = d.read(size)
                                    found = bytes.find(value[1])
                                    if found >= 0:
                                        f.write(bytes[:found+2])
                                        d.seek((offset+1)*size)
                                        drec = False
                                        count += 1
                                    else:
                                        f.write(bytes)
                    bytes = d.read(size)
                    progress_bar.update(1)
                    offset += 1
                d.close()
                print(f"\nRecovered {count} files in the deep search")
            except KeyboardInterrupt:
                progress_bar.close()
                print("Program stopped!")
                sys.exit()

def ft_get_from_disk(disk_path, selected_files):
    '''Get selected files from disk'''
    total = None
    for disks in psutil.disk_partitions():
        if disk_path in disks.device or disk_path in disks.mountpoint:
            total = psutil.disk_usage(disks.mountpoint).total
    if total is None:
        print("Error: Disk not found")
        sys.exit()
    if not os.path.exists(".\\Recovered_mft"):
            os.makedirs(".\\Recovered_mft")
    for key, value in selected_files.items():
        with open(rf"\\.\\{disk_path}", "rb") as d:
            bytes = d.read(value["offset"] + value["file_size"])
            with open(f".\\Recovered_mft\\{key}", "wb") as f:
                f.write(bytes[value["offset"]:])


def ft_get_file_attributes(disk_path, timelapse):
    '''Get file attributes from disk'''
    disk = rf"\\.\\{disk_path}"
    img_info = pytsk3.Img_Info(disk)
    fs_info = pytsk3.FS_Info(img_info)
    # Iterate through the files to recover from the entries of the MFT
    for file in good_recovered_files:
        try:
            unix_date = datetime.datetime.strptime(file[1], "%Y-%m-%d %H:%M:%S.%f").timestamp()
        except ValueError:
            unix_date = datetime.datetime.strptime(file[1], "%Y-%m-%d %H:%M:%S").timestamp()
        if unix_date >= timelapse:
            mft_file = fs_info.open(file[0])
            # Iterate through the attributes of the entries
            for attribute in mft_file:
                if attribute.info.type == pytsk3.TSK_FS_ATTR_TYPE_NTFS_DATA and attribute.info.name != b'Zone.Identifier':
                    # Iterate through the data runs of the $DATA attribute of each entry
                    for run in attribute:
                        cluster_start = run.addr * fs_info.info.block_size  # Offset in bytes
                        cluster_length = run.len * fs_info.info.block_size  # Length in bytes
                        recoverable[file[0].lstrip('/')] = {
                            "offset" : cluster_start, 
                            "file_size" : attribute.info.size, 
                            "cluster_size" : cluster_length,
                            "access_date" : file[1]}

def ft_select_options(stdscr):
    # Clear the screen
    stdscr.clear()

    selected_options = set()
    current_option = 0

    while True:
        # Clear the screen
        stdscr.clear()
        # Introductory message
        intro_message = "Select files to recover:"
        stdscr.addstr(0, 0, intro_message, curses.A_BOLD)

        # Display the options
        for i, (name, data) in enumerate(recoverable.items()):
            if i == current_option:
                # Display the current option with a highlight
                stdscr.addstr(i+1, 0, "> " + f"{name:35s}" + " <" + f" | size: {float(data['file_size']/1024):.2f}KB".ljust(20) +f"| access date: {data['access_date']}", curses.A_REVERSE)
            elif i in selected_options:
                # Display a tick after the selected options
                stdscr.addstr(i+1, 0,"* " + f"{name:35s}" + 2*" "+ f" | size: {float(data['file_size']/1024):.2f}KB".ljust(20) + f"| access date: {data['access_date']}")
            else:
                stdscr.addstr(i+1, 0, f"{name:35s}" + 4*" " + f" | size: {float(data['file_size']/1024):.2f}KB".ljust(20) + f"| access date: {data['access_date']}")

        # Display the "Start" option in bold letters without the asterisk
        start_option = "Start"
        if current_option == len(recoverable):
            stdscr.addstr(len(recoverable)+1, 0, "> " + start_option + " <", curses.A_REVERSE)
        else:
            stdscr.addstr(len(recoverable)+1, 0, start_option)

        # Refresh the screen
        stdscr.refresh()

        # Wait for user input
        try:
            key = stdscr.getch()
        except KeyboardInterrupt:
            print("Program stopped!")
            sys.exit()

        # Handle arrow key input
        if key == curses.KEY_UP:
            current_option = (current_option - 1) % (len(recoverable) + 1)
        elif key == curses.KEY_DOWN:
            current_option = (current_option + 1) % (len(recoverable) + 1)
        elif key == ord('\n'):  # Handle Enter key press
            if current_option == len(recoverable):
                break  # Break the loop if "Start" option is selected
            else:
                # Toggle the selection of the current option
                if current_option in selected_options:
                    selected_options.remove(current_option)
                else:
                    selected_options.add(current_option)

    if len(selected_options) > 0:
        # Print the selected options after the loop
        print("Recovered files:")
        for option_idx in selected_options:
            option_name = list(recoverable.keys())[option_idx]
            print(option_name)
        remove = []
        for i in range(len(recoverable)):
            if i not in selected_options:
                remove.append(i)
        items = list(recoverable.items())
        filtered_items = [item for i, item in enumerate(items, start=0) if i not in remove]
        selected_files = dict(filtered_items)
        ft_get_from_disk(disk, selected_files)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Tool for recovering recently deleted files on NTFS")
    parser.add_argument("disk", help="Path to the disk")
    parser.add_argument("-i", "--image", action="store", help="Create an image from a disk file")
    parser.add_argument("-t", "--timelapse", action="store", help="Time range in hours, default 24h" )
    arg = parser.parse_args()
    if arg.disk is None:
        print("A disk must be provided")
        sys.exit()
    if re.match(r'^[A-Z]:$', arg.disk) is None:
        print("Disk format must be uppercase letter followed by a colon (ex: 'D:')")
        sys.exit()
    try:
        date_format = "%d-%m-%Y"
        if arg.timelapse is not None:
            arg.timelapse = datetime.datetime.strptime(arg.timelapse, date_format).timestamp()
        else:
            arg.timelapse = time.time() - (24 * 60 * 60)
        return arg
    except Exception as e:
        print(f"Error: {e}")
        sys.exit()

if __name__ == "__main__":
    arg = parse_arguments()
    disk = arg.disk
    if arg.image:
        ft_create_image_from_disk(arg.disk, arg.image)
    ft_search_deleted_files(arg.disk)
    ft_get_file_attributes(arg.disk, arg.timelapse)
    curses.wrapper(ft_select_options)
    print("Do you want to do a deep search though the whole disk? [Y/N]")
    key = input()
    if key in ["y", "Y", "YES", "yes"]:
        ft_deep_search(arg.disk)
