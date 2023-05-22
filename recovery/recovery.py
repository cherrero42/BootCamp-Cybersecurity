#!/usr/bin/env python
# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    recovery.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cherrero <cherrero@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/05/18 13:09:23 by cherrero          #+#    #+#              #
#    Updated: 2023/05/21 21:19:50 by cherrero         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
import argparse
import winreg
import datetime
from datetime import datetime as datetimev
import os
import psutil
import sqlite3
import win32evtlog
import tempfile
import wmi

def extract_registry_changes(start_time, end_time):
    '''Extract the registry changes within the given time lapse'''
    key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
    key = winreg.HKEY_LOCAL_MACHINE

    try:
        registry_key = winreg.OpenKey(key, key_path, 0, winreg.KEY_READ)
        last_write_time = winreg.QueryInfoKey(registry_key)[2]
        if last_write_time/10000000 - 11644473600 > start_time.timestamp() and last_write_time/10000000 - 11644473600 < end_time.timestamp():
            print("\nRegistry branch 'CurrentVersionRun' was modified in the time lapse.")
            winreg.CloseKey(registry_key)

        print(f"\nLast modification date of 'CurrentVersionRun' registry branch: {datetimev.fromtimestamp(last_write_time/10000000 - 11644473600)}")
    except WindowsError:
        print("\nError accessing the 'CurrentVersionRun' registry branch.")

def extract_recent_files_reg(start_time, end_time):
    '''Extract the recent files within the given time lapse from registry'''
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs"
    key = winreg.HKEY_CURRENT_USER

    try:
        registry_key = winreg.OpenKey(key, key_path, 0, winreg.KEY_READ)
        num_entries = winreg.QueryInfoKey(registry_key)[1]

        print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
        print("\n\nRecent files:")
        for i in range(num_entries):
            value_name = winreg.EnumValue(registry_key, i)[0]

            try:
                timestamp = int(value_name)
                file_datetime = datetimev.fromtimestamp(timestamp)

                if start_time <= file_datetime <= end_time:
                    print(f"- {file_datetime}: {value_name}")
            except ValueError:
                # Ignore non-numeric value_names
                pass

        winreg.CloseKey(registry_key)
    except WindowsError:
        print("\nError accessing the recent files registry key.")

def extract_recent_files(start_time, end_time):
    '''Extract the recent files within the given time lapse'''
    recent_folder_path = os.path.expanduser("~\\AppData\\Roaming\\Microsoft\\Windows\\Recent")
  
    try:
        print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
        print("\n\nRecent files:")
        for filename in os.listdir(recent_folder_path):
            file_path = os.path.join(recent_folder_path, filename)
            modified_time = datetimev.fromtimestamp(os.path.getmtime(file_path))

            if start_time <= modified_time <= end_time:
                print(f"- {modified_time}: {filename}")
    except OSError:
        print("\nError accessing the Recent folder.\n")


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
        print(f"\nError accessing temporal files: {e}")

    return temporal_files

def extract_installed_programs(start_time, end_time):
    '''Extract the installed programs within the given time lapse'''

    # Define the registry key path for installed programs
    registry_key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"

    print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
    print("\n\nInstalled programs in the given time lapse:\n")
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

    print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
    print("\n\nRunning processes in the given time lapse:\n")
    try:
        # Iterate through all running processes
        for process in psutil.process_iter(['pid', 'name', 'create_time']):
            # Get the process creation time
            create_time = datetime.datetime.fromtimestamp(process.info['create_time'])
            # print(f"Process: {process.info['name']}, PID: {process.info['pid']}, Creation Time: {create_time}")

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

    print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
    print("\n\nBrowser history:" + str(start_time) + " - " + str(end_time))
    # Google Chrome history file path
    chrome_history_path = os.path.expanduser("~") + r"\AppData\Local\Google\Chrome\User Data\Default\History"
    # Mozilla Firefox history file path
    firefox_history_path = os.path.expanduser("~") + r"\AppData\Roaming\Mozilla\Firefox\Profiles"

    # Extract history from Google Chrome
    if os.path.isfile(chrome_history_path):
        chrome_history = extract_chrome_history(chrome_history_path, start_time, end_time)
        print("\nGoogle Chrome History:")
        print_history(chrome_history)

    # Extract history from Mozilla Firefox
    if os.path.isdir(firefox_history_path):
        firefox_profiles = os.listdir(firefox_history_path)
        for profile in firefox_profiles:
            profile_path = os.path.join(firefox_history_path, profile)
            places_file_path = os.path.join(profile_path, "places.sqlite")
            if os.path.isfile(places_file_path):
                firefox_history = extract_firefox_history(places_file_path, start_time, end_time)
                print("\nMozilla Firefox History:")
                print_history(firefox_history)

    extract_edge_browser_history(start_time, end_time)

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

    # Query to retrieve Firefox history with placeholders for parameters
    query = "SELECT url, title, last_visit_date FROM moz_places WHERE last_visit_date BETWEEN ? AND ?;"
    parameters = (start_time.timestamp() * 1000000, end_time.timestamp() * 1000000)

    cursor.execute(query, parameters)
    results = cursor.fetchall()

    history = []
    for row in results:
        url = row[0]
        title = row[1]
        visit_time = datetime.datetime.fromtimestamp(int(row[2] / 1000000)) if row[2] is not None else None
        history.append((url, title, visit_time))
        
    cursor.close()
    connection.close()

    return history

def extract_edge_browser_history(start_time, end_time):
    '''Extract the Microsoft Edge browser history within the given time lapse'''
    history_db_path = os.path.expanduser("~") + r"\AppData\Local\Microsoft\Edge\User Data\Default\History"

    try:
        connection = sqlite3.connect(history_db_path)
        cursor = connection.cursor()

        query = "SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC"
        cursor.execute(query)

        print("\nEdge browser history:")
        for row in cursor.fetchall():
            url = row[0]
            title = row[1]
            last_visit_time =  datetime.datetime(1601, 1, 1)  + datetime.timedelta(microseconds=row[2])

            if start_time <= last_visit_time <= end_time:
                print(f"URL: {url}")
                print(f"Title: {title}")
                print(f"Last Visit Time: {last_visit_time}")
                print()

        cursor.close()
        connection.close()
    except sqlite3.Error as e:
        print("\nError accessing Edge browser history database:", e)

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
        print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
        print("\n\nConnected devices:")
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

def extract_connected_devices():
    '''Extract the connected devices info'''
    c = wmi.WMI()

    print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
    print("Connected Devices:")
    for device in c.Win32_PnPEntity():
        if device.ConfigManagerErrorCode == 0:
            print(f"Device Name: {device.Name}")
            print(f"Description: {device.Description}")
            print(f"Manufacturer: {device.Manufacturer}")
            print()

def extract_event_logs(start_time, end_time):
    '''Extract the event logs within the given time lapse'''

    event_logs = []

    try:
        print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
        print("\n\nEvent logs:")
        # Open the Application event log
        hand = win32evtlog.OpenEventLog(None, "Application")

        # Iterate through the events in the log
        flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
        total_records = win32evtlog.GetNumberOfEventLogRecords(hand)
        print(f"\nTotal Records: {total_records}")
        events = win32evtlog.ReadEventLog(hand, flags, 0)

        while events:
            for event in events:
                # print(f"Event ID: {event.EventID}")
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

if __name__ == "__main__":

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Recovery system info within a given time lapse')
    parser.add_argument('-s', '--start_date', type=str, help='Start date in YYYY-MM-DD format')
    parser.add_argument('-e', '--end_date', type=str, help='End date in YYYY-MM-DD format')
    args = parser.parse_args()

    # Convert input dates to datetime objects
    try:
        if args.start_date and args.end_date:
            start_time = datetime.datetime.strptime(args.start_date, '%Y-%m-%d')
            end_time = datetime.datetime.strptime(args.end_date, '%Y-%m-%d')
        elif args.end_date:
            # Define the start and end times for the time lapse - last 24 hours
            end_time = datetime.datetime.strptime(args.end_date, '%Y-%m-%d')
            start_time = end_time - datetime.timedelta(hours=24)
        elif args.start_date:
            start_time = datetime.datetime.strptime(args.start_date, '%Y-%m-%d')
            end_time = datetime.datetime.now()
        else:
            start_time = datetime.datetime.now() - datetime.timedelta(hours=1)
            end_time = datetime.datetime.now()
    except ValueError:
        print("\nInvalid date format. Please use YYYY-MM-DD format.")
        sys.exit()

    print("\nShow recovery info from: " + str(start_time) + " to " + str(end_time))

    # Extract the registry changes within the given time lapse
    extract_registry_changes(start_time, end_time)


    # Extract the recent files within the given time lapse in registry 
    # extract_recent_files_reg(start_time, end_time)

    # Extract the recent files within the given time lapse
    extract_recent_files(start_time, end_time)

    # Extract the temporal files within the given time lapse
    temporal_files = extract_temporal_files(start_time, end_time)

    # Print the temporal files
    print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
    print("\n\nTemporal files:")
    for file in temporal_files:
        print(file)

    # Extract the installed programs within the given time lapse
    extract_installed_programs(start_time, end_time)

    # Extract the running processes within the given time lapse
    running_processes = extract_running_processes(start_time, end_time)

    # Print the list of running processes
    for process in running_processes:
        print(f"Process: {process['name']}, PID: {process['pid']}, Creation Time: {process['create_time']}")

    # Extract the web browser history within the given time lapse
    extract_browser_history(start_time, end_time)


    # Extract the connected devices    
    extract_connected_devices()

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
    
