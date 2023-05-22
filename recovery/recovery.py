#!/usr/bin/env python
# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    recovery.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cherrero <cherrero@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/05/18 13:09:23 by cherrero          #+#    #+#              #
#    Updated: 2023/05/19 21:09:50 by cherrero         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import argparse
import winreg
import datetime
import os
import psutil
import sqlite3
import win32evtlog
import tempfile


def extract_registry_changes(start_time, end_time):
    '''Extract the registry changes within the given time lapse'''

    print("Registry changes:" + str(start_time) + " " + str(end_time))
    # Define the registry branch path
    registry_key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"

    try:
        # Open the registry key for reading
        registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_key_path, 0, winreg.KEY_READ)

        # Get the number of subkeys under the registry branch
        num_subkeys = winreg.QueryInfoKey(registry_key)[0]
        print("Number of subkeys: {}".format(num_subkeys))

        # Iterate through the subkeys and extract the changes within the given time lapse
        for i in range(num_subkeys):
            subkey_name = winreg.EnumKey(registry_key, i)
            subkey_path = registry_key_path + "\\" + subkey_name

            # Open the subkey for reading
            subkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, subkey_path, 0, winreg.KEY_READ)


            # for key in key_types:
            #     # Data
            #     handler = winreg.OpenKey(key, "Software\\Microsoft\\Windows\\CurrentVersion\\Run")
            #     reg_key_ts = windows_ticks_to_unix_seconds(winreg.QueryInfoKey(handler)[2])
                
            #     # Date
            #     dt = datetime.date.fromtimestamp(reg_key_ts)
                
            #     # Info collection
            #     regis = ["Registry branches changes date (Software\\Microsoft\\Windows\\CurrentVersion\\Run)", dt]
            #     insertRow(tb_name, regis)





            # Get the last write time of the subkey
            last_write_time = winreg.QueryInfoKey(subkey)[2]
            last_write_time = datetime.datetime.fromtimestamp(last_write_time)

            # Check if the last write time is within the given time lapse
            if start_time <= last_write_time <= end_time:
                print(f"Subkey: {subkey_path}")
                print(f"Last write time: {last_write_time}")
                print()

            # Close the subkey
            winreg.CloseKey(subkey)

        # Close the registry key
        winreg.CloseKey(registry_key)

    except OSError as e:
        print(f"Error accessing the registry: {e}")



def extract_recent_files(start_time, end_time):
    '''Extract the recent files within the given time lapse'''

    recent_files = []


# # HOME = os.getenv("HOME")
    # PATH_RECENT = HOME + "\AppData\Roaming\Microsoft\Windows\Recent"


    # Get the user's home directory
    home_dir = os.path.expanduser("~")
    recent_dir = home_dir + "\AppData\Roaming\Microsoft\Windows\Recent"
    
    # print("Home directory: {}".format(home_dir))






    try:
        # Walk through the home directory and its subdirectories
        # for file in os.listdir(home_dir):
		    # file_path = os.path.join(path, file_name)
		    # if os.path.isdir(file_path):
        for root, dirs, files in os.walk(recent_dir):
            for file in files:
                try:
                    # print(recent_dir + "\" + str(file))
                    # r_time = os.path.getmtime(recent_dir + "\\" + str(file))
                    last_access_time = datetime.datetime.fromtimestamp(os.path.getmtime(recent_dir + "\\" + str(file)))
                    # print(r_time)
                    # print(f_time)

                    # regis = []
                    # regis.append(f)
                    # regis.append(f_time)
                    # insertRow(tb_name, regis)
                    # Check if the last access time is within the given time lapse
                    if start_time <= last_access_time <= end_time:
                        recent_files.append(recent_dir + "\\" + str(file))
                except:
                    pass

                # Get the path of the file
                # file_path = os.path.join(home_dir, file)
                # print("File path: {}".format(file_path))

                # # Get the last access time of the file
                # last_access_time = datetime.datetime.fromtimestamp(os.path.getatime(file_path))
                # stat_info = os.stat(file_path)
                # last_access_time = datetime.datetime.fromtimestamp(stat_info.st_atime)


                # # Obtener el tiempo de acceso y el tiempo de modificación del archivo
                # access_time_seconds = os.path.getatime(file_path)
                # modify_time_seconds = os.path.getmtime(file_path)

                # # Convertir los tiempos de acceso y modificación a objetos datetime
                # access_datetime = datetime.datetime.fromtimestamp(access_time_seconds)
                # modify_datetime = datetime.datetime.fromtimestamp(modify_time_seconds)

                # # Obtener la última fecha de acceso del archivo
                # last_access_time = max(access_datetime, modify_datetime)

                # Obtener el tiempo de acceso en segundos desde la época
                # access_time_seconds = os.path.getatime(file_path)

                # # Convertir el tiempo de acceso a un objeto datetime
                # last_access_time = datetime.datetime.fromtimestamp(access_time_seconds)

                # print("Last access time: {}".format(last_access_time))


    except OSError as e:
        print(f"Error accessing files: {e}")

    return recent_files


def extract_temporal_files(start_time, end_time):
    '''Extract temporal files within the given time lapse'''

    temporal_files = []

    try:
        # Get the system's temporary directory
        temp_dir = tempfile.gettempdir()

        # Iterate through all files in the temporary directory
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                file_create_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path))

                # Check if the file creation time is within the given time lapse
                if start_time <= file_create_time <= end_time:
                    temporal_files.append(file_path)

    except Exception as e:
        print(f"Error accessing temporal files: {e}")

    return temporal_files
    # HOME = os.getenv("HOME")
    # PATH_RECENT = HOME + "\AppData\Local\Temp"


def extract_installed_programs(start_time, end_time):
    '''Extract the installed programs within the given time lapse'''

    # Define the registry key path for installed programs
    registry_key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"

    try:
        # Open the registry key for reading
        registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_key_path, 0, winreg.KEY_READ)

        # Get the number of subkeys under the registry branch
        num_subkeys = winreg.QueryInfoKey(registry_key)[0]

        # Iterate through the subkeys and extract the installed programs within the given time lapse
        for i in range(num_subkeys):
            subkey_name = winreg.EnumKey(registry_key, i)
            subkey_path = registry_key_path + "\\" + subkey_name

            # Open the subkey for reading
            subkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, subkey_path, 0, winreg.KEY_READ)

            # Check if the subkey has an "InstallDate" value
            try:
                install_date = winreg.QueryValueEx(subkey, "InstallDate")[0]

                # Convert the install date to a datetime object
                install_date = datetime.datetime.strptime(install_date, "%Y%m%d")

                # Check if the install date is within the given time lapse
                if start_time <= install_date <= end_time:
                    program_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                    program_version = winreg.QueryValueEx(subkey, "DisplayVersion")[0]
                    print(f"Program Name: {program_name}")
                    print(f"Version: {program_version}")
                    print()

            except FileNotFoundError:
                pass  # Ignore subkeys without an "InstallDate" value

            # Close the subkey
            winreg.CloseKey(subkey)

        # Close the registry key
        winreg.CloseKey(registry_key)

    except OSError as e:
        print(f"Error accessing the registry: {e}")


def extract_running_processes(start_time, end_time):
    '''Extract the running processes within the given time lapse'''

    running_processes = []

    try:
        # Iterate through all running processes
        for process in psutil.process_iter(['pid', 'name', 'create_time']):
            # Get the process creation time
            create_time = datetime.datetime.fromtimestamp(process.info['create_time'])

            # Check if the creation time is within the given time lapse
            if start_time <= create_time <= end_time:
                running_processes.append({
                    'pid': process.info['pid'],
                    'name': process.info['name'],
                    'create_time': create_time
                })

    except psutil.Error as e:
        print(f"Error accessing running processes: {e}")

    return running_processes

def extract_browser_history(start_time, end_time):
    '''Extract the web browser history within the given time lapse'''

    print("Browser history:" + str(start_time) + " " + str(end_time))
    # Google Chrome history file path
    chrome_history_path = os.path.expanduser("~") + r"\AppData\Local\Google\Chrome\User Data\Default\History"
    # Mozilla Firefox history file path
    firefox_history_path = os.path.expanduser("~") + r"\AppData\Roaming\Mozilla\Firefox\Profiles"

    # Extract history from Google Chrome
    if os.path.isfile(chrome_history_path):
        chrome_history = extract_chrome_history(chrome_history_path, start_time, end_time)
        print("Google Chrome History:")
        print_history(chrome_history)

    # Extract history from Mozilla Firefox
    if os.path.isdir(firefox_history_path):
        firefox_profiles = os.listdir(firefox_history_path)
        for profile in firefox_profiles:
            profile_path = os.path.join(firefox_history_path, profile)
            places_file_path = os.path.join(profile_path, "places.sqlite")
            if os.path.isfile(places_file_path):
                firefox_history = extract_firefox_history(places_file_path, start_time, end_time)
                print("Mozilla Firefox History:")
                print_history(firefox_history)

def extract_chrome_history(history_path, start_time, end_time):
    '''Extract the Google Chrome history within the given time lapse'''

    connection = sqlite3.connect(history_path)
    cursor = connection.cursor()

    # Query to retrieve Chrome history
    query = f"SELECT url, title, visit_time FROM urls WHERE visit_time BETWEEN {start_time.timestamp()}*1000000 AND {end_time.timestamp()}*1000000;"

    cursor.execute(query)
    results = cursor.fetchall()

    history = []
    for row in results:
        url = row[0]
        title = row[1]
        visit_time = datetime.datetime.fromtimestamp(int(row[2] / 1000000))
        history.append((url, title, visit_time))

    cursor.close()
    connection.close()

    return history

def extract_firefox_history(history_path, start_time, end_time):
    '''Extract the Mozilla Firefox history within the given time lapse'''

    connection = sqlite3.connect(history_path)
    cursor = connection.cursor()

    # Query to retrieve Firefox history
    query = f"SELECT url, title, last_visit_date FROM moz_places WHERE last_visit_date BETWEEN {start_time.timestamp()}000000 AND {end_time.timestamp()}000000;"

    cursor.execute(query)
    results = cursor.fetchall()

    history = []
    for row in results:
        url = row[0]
        title = row[1]
        visit_time = datetime.datetime.fromtimestamp(int(row[2] / 1000000))
        history.append((url, title, visit_time))

    cursor.close()
    connection.close()

    return history

def print_history(history):
    '''Print the web browser history'''

    for entry in history:
        url = entry[0]
        title = entry[1]
        visit_time = entry[2]
        print(f"URL: {url}")
        print(f"Title: {title}")
        print(f"Visit Time: {visit_time}")
        print()


def extract_connected_devices(start_time, end_time):
    '''Extract the connected devices info within the given time lapse'''

    connected_devices = []

    try:
        # Get the active network connections
        connections = psutil.net_connections()

        # Get the system boot time
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())

        # Iterate through the active connections and extract the connected devices within the given time lapse
        for conn in connections:
            create_time = boot_time + datetime.timedelta(seconds=conn.pid)

            # Check if the connection creation time is within the given time lapse
            if start_time <= create_time <= end_time:
                remote_address = conn.raddr
                remote_ip = remote_address.ip if remote_address.ip else "Unknown"
                remote_port = remote_address.port if remote_address.port else "Unknown"

                device = {
                    'local_address': conn.laddr.ip,
                    'local_port': conn.laddr.port,
                    'remote_address': remote_ip,
                    'remote_port': remote_port,
                    'create_time': create_time
                }
                connected_devices.append(device)

    except psutil.Error as e:
        print(f"Error accessing connected devices: {e}")

    return connected_devices


# def extract_connected_devices2(start_time, end_time):
#     connected_devices = []

#     try:
#         # Get the active network connections
#         connections = psutil.net_connections()

#         # Get the system boot time
#         boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())

#         # Iterate through the active connections and extract the connected devices within the given time lapse
#         for conn in connections:
#             create_time = boot_time + datetime.timedelta(seconds=conn.pid)

#             # Check if the connection creation time is within the given time lapse
#             if start_time <= create_time <= end_time:
#                 device = {
#                     'local_address': conn.laddr.ip,
#                     'local_port': conn.laddr.port,
#                     'remote_address': conn.raddr.ip,
#                     'remote_port': conn.raddr.port,
#                     'create_time': create_time
#                 }
#                 connected_devices.append(device)

#     except psutil.Error as e:
#         print(f"Error accessing connected devices: {e}")

#     return connected_devices


# def check_connected_devices3():
# 	c = wmi.WMI()
# 	devices = c.Win32_PnPEntity()
# 	connected_devices = []
# 	for device in devices:
# 		if device.ConfigManagerErrorCode == 0:
# 			connected_devices.append(device)
# 	if connected_devices:
# 		print("Connected Devices:")
# 		for device in connected_devices:
# 			print(f"Name: {device.Name}")
# 			print(f"Description: {device.Description}")
# 			print(f"Status: {device.Status}")
# 			print("---")

def extract_event_logs(start_time, end_time):
    '''Extract the event logs within the given time lapse'''

    event_logs = []

    try:
        # Open the Application event log
        hand = win32evtlog.OpenEventLog(None, "Application")

        # Iterate through the events in the log
        flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
        total_records = win32evtlog.GetNumberOfEventLogRecords(hand)
        events = win32evtlog.ReadEventLog(hand, flags, 0)

        while events:
            for event in events:
                event_time = event.TimeGenerated.Format()  # Get the event log timestamp as string

                # Parse the event time using a custom format
                event_datetime = datetime.datetime.strptime(event_time, "%a %b %d %H:%M:%S %Y")

                # Check if the event time is within the given time lapse
                if start_time <= event_datetime <= end_time:
                    event_logs.append({
                        'TimeGenerated': event_time,
                        'SourceName': event.SourceName,
                        'EventID': event.EventID,
                        'EventType': event.EventType,
                        'EventCategory': event.EventCategory,
                        'Strings': event.StringInserts
                    })

            events = win32evtlog.ReadEventLog(hand, flags, 0)

        # Close the event log
        win32evtlog.CloseEventLog(hand)

    except Exception as e:
        print(f"Error accessing event logs: {e}")

    return event_logs


# def extract_event_logs2(start_time, end_time):
#     '''Extract the event logs within the given time lapse'''
#     event_logs = []

#     try:
#         # Open the Application event log
#         hand = win32evtlog.OpenEventLog(None, "Application")

#         # Iterate through the events in the log
#         flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
#         total_records = win32evtlog.GetNumberOfEventLogRecords(hand)
#         events = win32evtlog.ReadEventLog(hand, flags, 0)

#         while events:
#             for event in events:
#                 event_time = event.TimeGenerated.Format()
#                 event_datetime = datetime.datetime.strptime(event_time, "%Y%m%d%H%M%S")

#                 # Check if the event time is within the given time lapse
#                 if start_time <= event_datetime <= end_time:
#                     event_logs.append({
#                         'TimeGenerated': event_time,
#                         'SourceName': event.SourceName,
#                         'EventID': event.EventID,
#                         'EventType': event.EventType,
#                         'EventCategory': event.EventCategory,
#                         'Strings': event.StringInserts
#                     })

#             events = win32evtlog.ReadEventLog(hand, flags, 0)

#         # Close the event log
#         win32evtlog.CloseEventLog(hand)

#     except Exception as e:
#         print(f"Error accessing event logs: {e}")

#     return event_logs







if __name__ == "__main__":

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Recovery system info within a given time lapse')
    parser.add_argument('-s', '--start_date', type=str, help='Start date in YYYY-MM-DD format')
    parser.add_argument('-e', '--end_date', type=str, help='End date in YYYY-MM-DD format')
    args = parser.parse_args()

    # Convert input dates to datetime objects
    if args.start_date and args.end_date:
        start_time = datetime.datetime.strptime(args.start_date, '%Y-%m-%d')
        end_time = datetime.datetime.strptime(args.end_date, '%Y-%m-%d')
    else:
        # Define the start and end times for the time lapse - last 24 hours
        # start_time = datetime.datetime(2023, 5, 10)
        end_time = datetime.datetime(2023, 5, 23)
        start_time = end_time - datetime.timedelta(hours=28)

    print("Start time: {}".format(start_time))
    print("End time: {}".format(end_time))
    # Extract the registry changes within the given time lapse
    extract_registry_changes(start_time, end_time)


    # Extract the recent files within the given time lapse
    recent_files = extract_recent_files(start_time, end_time)

    # Print the list of recent files
    for file in recent_files:
        print(file)

    # Extract the temporal files within the given time lapse
    temporal_files = extract_temporal_files(start_time, end_time)

    # Print the temporal files
    for file in temporal_files:
        print(file)

    # Extract the installed programs within the given time lapse
    extract_installed_programs(start_time, end_time)

    # Extract the running processes within the given time lapse
    running_processes = extract_running_processes(start_time, end_time)

    # Print the list of running processes
    for process in running_processes:
        print(f"PID: {process['pid']}")
        print(f"Name: {process['name']}")
        print(f"Creation Time: {process['create_time']}")
        print()

    # Extract the web browser history within the given time lapse
    extract_browser_history(start_time, end_time)

    # Extract the connected devices within the given time lapse
    # connected_devices = extract_connected_devices(start_time, end_time)

    # # Print the list of connected devices
    # for device in connected_devices:
    #     print(f"Local Address: {device['local_address']}")
    #     print(f"Local Port: {device['local_port']}")
    #     print(f"Remote Address: {device['remote_address']}")
    #     print(f"Remote Port: {device['remote_port']}")
    #     print(f"Creation Time: {device['create_time']}")
    #     print()

    # check_connected_devices3()
#       File "\\vboxsrv\intere\recovery.py", line 305, in check_connected_devices3
#     c = wmi.WMI()
# NameError: name 'wmi' is not defined

    # Extract the event logs within the given time lapse
    event_logs = extract_event_logs(start_time, end_time)

    # Print the event logs
    for log in event_logs:
        print(f"Time Generated: {log['TimeGenerated']}")
        print(f"Source Name: {log['SourceName']}")
        print(f"Event ID: {log['EventID']}")
        print(f"Event Type: {log['EventType']}")
        print(f"Event Category: {log['EventCategory']}")
        # print(f"Strings: {', '.join(log['Strings'])}")
            # Check if 'Strings' is iterable before using 'join'
        if isinstance(log['Strings'], list):
            print(f"Strings: {', '.join(log['Strings'])}")
        else:
            print(f"Strings: {log['Strings']}")

        print()
    