#!/usr/bin/env python3
# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    irondome.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: lguisado <lguisado@student.42.fr>          +#+  +:+       +#+         #
#        cherrero <cherrero@student.42.fr>        +#+#+#+#+#+   +#+            #
#    Created: 2023/05/07 14:27:55                      #+#    #+#              #
#    Updated: 2023/05/15 19:05:12                     ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
try:
	import os
	import psutil
	import shutil
	import hashlib
	import logging
	import argparse
	from pathlib import Path
	from datetime import datetime, timedelta
	import pandas as pd
	import hashlib
	import magic
	import subprocess
	import math
	import string
	import random
	from cryptography.fernet import Fernet
	import daemon
	from watchdog.observers import Observer
	from watchdog.events import FileSystemEventHandler
	import time
	import platform
except ModuleNotFoundError:
 	sys.exit("\nError: Some libraries were not found. Check requirements.")

dir_master = '/bootcamp/iron_dome/'
path_master = str(Path.home()) + dir_master
dir_backup = '/bootcamp/iron_dome/alert_zone_backup/'
path_backup = str(Path.home()) + dir_backup
dir_demo = '/bootcamp/iron_dome/infection/'
path_demo = str(Path.home()) + dir_demo

version = 'irondome 1.0.0'
log_file = '/var/log/irondome/irondome.log'
version = 'irondome 1.0.0'
file_csv = "_files_info.csv"
time_backup = 9999999999 # seconds

limit_net_bytes = 70000000000  #  GB
limit_percent_cpu = 60
limit_percent_mem = 5
limit_reads = 10
limit_disk_reads = 3
file_entropy_dict = {}

def ft_encrypt_file(file):
	'''Encrypt file for testing proposal'''
	try:
		with open(file, 'rb') as f:
			data = f.read()
		encrypted = Fernet(Fernet.generate_key()).encrypt(data)
		with open(file + ".ft", 'wb') as f:
			f.write(encrypted)
		return
	except:
		sys.exit("\nError encrypting file.")

def ft_generate_random_string(length):
	'''Generate random string for testing proposal'''
	letters = string.ascii_lowercase
	return ''.join(random.choice(letters) for _ in range(length))

def ft_create_random_files(num_files, file_size, directory):
	'''Create random files for testing proposal'''
	if not os.path.exists(directory):
		os.makedirs(directory)

	for i in range(num_files):
		file_name = ft_generate_random_string(10)  # random name
		file_path = os.path.join(directory, file_name)

		with open(file_path, 'wb') as file:
			file.write(os.urandom(file_size))  # random content

def ft_log_write(txt, type='a'):
	'''Write log'''
	try:
		with open(log_file, type) as f:
			f.write(txt + "\n")
	except:
		pass

def ft_get_mod_date(file):
	'''Get modification date of file'''
	modif_date = os.path.getmtime(file)
	return datetime.fromtimestamp(modif_date)

def ft_get_hash(file):
	'''Get hash of file'''
	BUF_SIZE = 65536  # buffer size
	sha256 = hashlib.sha256()

	with open(file, "rb") as file:
		while True:
			data = file.read(BUF_SIZE)
			if not data:
				break
			sha256.update(data)

	return sha256.hexdigest()

def ft_get_magic2(file):
	'''Get magic of file'''
	magic_output = subprocess.check_output(['file', '--mime-type', '--brief', file])
	magic_hash = magic_output.decode().strip()
	return magic_hash

def ft_get_magic(file):
	'''Get magic of file'''
	mime = magic.Magic(mime=True)
	return(mime.from_file(file))

def ft_backup(file):
	'''Backup file to dir_backup'''
	ft_log_write("Backup: " + file + " - " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
	try:
		shutil.copy2(path_master + args.critical_zone + '/' + file , path_backup + file + "_" + datetime.now().strftime("%d%m%Y%H%M%S"))
	except Exception:
		ft_log_write("Error backup: " + file + " - " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

def ft_delete_name(file):
	'''Delete name of file in file_csv'''
	df = pd.read_csv(path_master + file_csv)
	if file in df['File'].values:
		df = df.drop(df[df['File'] == file].index)
		df.to_csv(path_master + file_csv, index=False)
		ft_log_write("File deleted in file_csv: " + file + " - " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
	else:
		ft_log_write("File not found in file_csv: " + file + " - " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

def ft_get_used_memory():
	'''Get total memory used'''
	mem = psutil.virtual_memory()
	used_memory = mem.used / (1024 ** 3)  # GB
	return used_memory

def ft_get_total_cpu():
	'''Get total cpu used'''
	cpu_percent = psutil.cpu_percent()
	return cpu_percent

def ft_get_disk_reads():
	'''Get disk reads from /proc/diskstats'''
	with open('/proc/diskstats', 'r') as f:
		lines = f.readlines()
		disk_reads = 0
		for line in lines:
			fields = line.split()
			if len(fields) >= 4 and fields[3].startswith('vd'):
				disk_reads += int(fields[12])
		return disk_reads

def ft_check_activity_system():
	'''Check activity in processes'''
	# we use psutil.process_iter() to iterate through all running processes and check their CPU and memory usage.
	#   If a process is using more than x50% CPU or memory and its name contains "openssl", "gnutls", or "crypt", 
	#   we log a message indicating that intensive cryptographic activity has been detected.
	global current_reads
	if ft_get_total_cpu() > limit_percent_cpu:
		ft_log_write("Alert CPU!: " + str(ft_get_total_cpu()) + " - " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
		logging.warning(f'Intensive CPU usage detected')
	if ft_get_used_memory() > limit_percent_mem:
		ft_log_write("Alert memory!: " + str(ft_get_used_memory()) + " - " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
		logging.warning(f'Intensive memory usage detected')

	if (ft_get_disk_reads() - current_reads) > limit_disk_reads:
		ft_log_write("Alert disk reads!: " + str(ft_get_disk_reads() - current_reads) + " - " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
		current_reads = ft_get_disk_reads()
	
	processes = psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent'])
	for proc in processes:
		try:
			process_name = proc.info['name']
			cpu_percent = proc.info['cpu_percent']
			memory_percent = proc.info['memory_percent']

			if 'openssl' in process_name or 'gnutls' in process_name or 'crypt' in process_name:
				ft_log_write("Alert!: " + proc.info['name'] + " CPU: " + str(cpu_percent)  + " Memory: " + str(memory_percent) + " - " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
				logging.warning(f'Intensive cryptographic activity detected in process {process_name}')
		except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
			pass

	network_io = psutil.net_io_counters()
	bytes_sent = network_io.bytes_sent
	bytes_received = network_io.bytes_recv
	if bytes_sent > limit_net_bytes or bytes_received > limit_net_bytes:
		logging.warning(f'High network I/O activity detected')
	if psutil.Process(os.getpid()).memory_info().rss > 100000000:
		logging.warning('Memory usage exceeded 100 MB')

def ft_calculate_entropy(data):
	'''Calculate entropy of data'''
	# This loop calculates the entropy using the information theory formula, where each probability is weighted by its base 2 logarithm and added to the total entropy.
	entropy = 0
	total_bytes = len(data)
	freq_dict = {}
	
	for byte in data:
		freq_dict[byte] = freq_dict.get(byte, 0) + 1
	
	for count in freq_dict.values():
		probability = count / total_bytes
		entropy -= probability * math.log2(probability)
	return entropy

def ft_is_encrypted_file(file_path):
	'''Check if the file has an extension commonly associated with encrypted files'''
	encrypted_extensions = ['.enc', '.crypt', '.gpg']
	if any(file_path.endswith(ext) for ext in encrypted_extensions):
		return True

	# Use the 'python-magic' library to get information about the file type
	try:
		file_type = magic.from_file(file_path)
	except:
		return False
	
	# Check if the file type is related to encryption or encryption
	encrypted_file_types = ['encrypted', 'crypt', 'PGP', 'GPG']
	if any(file_type.lower().find(keyword) != -1 for keyword in encrypted_file_types):
		return True

	return False

def ft_valid_file(file, extensions=None):
	if not extensions:
		return True
	else:
		for ext in extensions:
			if file.endswith(ext):
				return True
	return False

def ft_get_file_entropy(file_path):
	'''Get entropy of file'''
	try:
		with open(file_path, 'rb') as file:
			data = file.read()
			entropy = ft_calculate_entropy(data)
			return entropy
	except:
		ft_log_write("Error get entropy: " + file_path + " - " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

def ft_detect_entropy_changes(directory_path, extensions=None):
	'''Detect entropy changes in files'''
	file_entropy_dict_changes = {}
	for root, dirs, files in os.walk(directory_path):
		for file in files:
			if not ft_valid_file(file, extensions):
				continue
			file_path = os.path.join(root, file)
			entropy = ft_get_file_entropy(file_path)
			if file_path not in file_entropy_dict or file_entropy_dict[file_path] != entropy:
					file_entropy_dict[file_path] = entropy
					file_entropy_dict_changes[file_path] = entropy
					ft_log_write("Entropy change detected in: " + file_path + " - " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))	
	return file_entropy_dict_changes

class FileEventHandler(FileSystemEventHandler):
	'''Class to monitor files'''
	def __init__(self):
		self.read_count = 0
		self.deleted_file = None
		self.created_file = None

	def on_deleted(self, event):
		if not event.is_directory:
			self.deleted_file = event.src_path
			self.read_count += 1

	def on_created(self, event):
		if not event.is_directory:
			self.created_file = event.src_path
			self.read_count += 1

	def on_modified(self, event):
		# Increment the read count when a file or directory is modified
		self.read_count += 1
		
def ft_start_monitoring_files(path, extensions=None):
	''''main monitoring process'''
	global last_time_backup
	event_handler = FileEventHandler()
	observer = Observer()
	observer.schedule(event_handler, path, recursive=False)
	observer.start()
	
	try:
		while True:
			if last_time_backup + timedelta(seconds=time_backup) < datetime.now():
				for file in os.listdir(path_master + args.critical_zone):
					if not ft_valid_file(file, extensions):
						continue
					ft_backup(file)
				last_time_backup = datetime.now()
			ft_detect_entropy_changes(path_master + args.critical_zone, args.extensions)
			ft_check_files(path_master + args.critical_zone, args.extensions)
			ft_check_activity_system()
			# Monitor disk read usage every 1 seconds
			time.sleep(0.00001)
			if event_handler.read_count > limit_reads:
				ft_log_write("Alert! Disk read count for directory " + path_master + args.critical_zone + ": " + str(event_handler.read_count) + " - " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
			if event_handler.deleted_file:
				ft_log_write("Alert! File deleted: " + event_handler.deleted_file + " - " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
				ft_delete_name(event_handler.deleted_file.split('/')[-1])
			if event_handler.created_file:
				ft_log_write("Alert! File created: " + event_handler.created_file + " - " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
				if ft_is_encrypted_file(event_handler.created_file):
					ft_log_write("Alert! File possibly crypted: " + event_handler.created_file + " - " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
					logging.warning(f'Intensive cryptographic activity detected in file {event_handler.created_file}')
			event_handler.read_count = 0
			event_handler.deleted_file = None
			event_handler.created_file = None
	except KeyboardInterrupt:
		observer.stop()
	except Exception:
		ft_log_write("Error monitoring alert files: " + " - " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
	observer.join()

	return event_handler.deleted_file, event_handler.created_file


def ft_check_files(critical_zone, extensions=None):
	'''Checking files in critical_zone'''
	try:
		# check file CSV
		file_name = os.path.isfile(path_master + file_csv)
		# DataFrame
		if file_name:
			df = pd.read_csv(path_master + file_csv)
		else:
			# empty DataFrame
			df = pd.DataFrame(columns=["File", "Modif_date", "Hash", "Magic"])
		for file in os.listdir(critical_zone):
			if not ft_valid_file(file, extensions):
				continue
			dir = os.path.join(critical_zone, file)
			if os.path.isfile(dir):
				modif_date = ft_get_mod_date(dir)
				file_name = df['File'] == file
				if file_name.any():
					# check modif_date of file
					file_index = file_name.idxmax()
					if file and (str(modif_date) in (df.loc[df['File'] == file]).values):
						continue
					else:
						# hash file
						file_hash = ft_get_hash(dir)

						# magic of file
						file_magic = ft_get_magic(dir)

						# update information in DataFrame
						df.loc[file_index, 'Modif_date'] = modif_date
						df.loc[file_index, 'Hash'] = file_hash
						df.loc[file_index, 'Magic'] = file_magic
						ft_log_write("File modified: " + file + " - " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

						if file and (str(file_magic) in (df.loc[df['Magic'] == file_magic]).values):
							# file is correctly modified
							ft_backup(file)
						else:
							# magic changed: illegal operation
							ft_log_write("Illegal operation in: " + file + " - " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
				else:
					file_hash = ft_get_hash(dir)
					file_magic = ft_get_magic(dir)
					# add information to DataFrame
					df.loc[len(df.index)] = [file, modif_date, file_hash, file_magic]
					ft_backup(file)
					ft_log_write("File added: " + file + " - " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
			else:
				pass
		# Save DataFrame to file CSV
		df.to_csv(path_master + file_csv, index=False)
	except Exception:
		ft_log_write("Error checking files: " + file + " - " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

def main():
# config context of the daemon
	with daemon.DaemonContext():
		while True:
		# runs the main code in the context of the daemon
			try:
				ft_log_write("Daemon started with pid: " + str(os.getpid()) + " - " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
				ft_start_monitoring_files(path_master + args.critical_zone, args.extensions)
				main()
			except Exception:
				ft_log_write("Error monitoring files: " + " - " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
				sys.exit(1)


if __name__ == '__main__':
	global last_time_backup, current_reads

	parser = argparse.ArgumentParser(description='Monitor a critical zone for file changes and anomalies')
	parser.add_argument('critical_zone', help='Path to the critical zone to monitor', default='alert_zone')
	parser.add_argument('-e', '--extensions', help='Comma-separated list of file extensions to monitor')
	parser.add_argument('-d', '--demo_mode', help='generating demo cryptographic activity', action="store_true")
	parser.add_argument('-b', '--backup_time', type=int, help='period backups time in seconds')

	if os.geteuid() != 0:
		print('This program must be run as root')
		sys.exit(1)

	if not platform.system() == "Linux":
		print('irondome is linux-specific, and does not work on %s' %platform.system())
		sys.exit(1)

	args = parser.parse_args()
	
	if args.demo_mode:
		ft_log_write("Demo mode, generating demo cryptographic activity")
		num_files = 50
		file_size = 1024  # size in bytes

		ft_create_random_files(num_files, file_size, path_demo)
		for file_name in os.listdir(path_demo):
			file_path = os.path.join(path_demo, file_name)
			if os.path.isfile(file_path):
				ft_encrypt_file(file_path)
		sys.exit(0)

	ft_log_write("Version: " + version, "w")
	ft_log_write("[irondome] " + "Critical zone: " + path_master + args.critical_zone + " - " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n")
	last_time_backup = datetime.now()

	try:
		os.makedirs(os.path.dirname(log_file))
	except:
		if not os.path.exists(os.path.dirname(log_file)):
			ft_log_write("Error in log directory")
			sys.exit(1)

	try:
		os.makedirs(path_backup)
	except:
		if not os.path.exists(path_backup):
			ft_log_write("Error in backup directory")
			sys.exit(1)

	if not os.path.exists(path_master + args.critical_zone):
		ft_log_write("Error in critical zone")
		sys.exit(1)
		
	if args.extensions is None:
		ft_log_write("All extensions are observed")
	else:
		args.extensions = args.extensions.split(',') if args.extensions else None
		ft_log_write("Extensions observed: " + str(args.extensions))

	if args.backup_time is not None:
		time_backup = args.backup_time
		ft_log_write("Backup time: " + str(time_backup) + " seconds")

	logging.basicConfig(filename=log_file, level=logging.INFO)

	current_reads = ft_get_disk_reads()

	main()
