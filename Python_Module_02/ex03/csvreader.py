#!/usr/bin/env python
# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    csvreader.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cherrero <cherrero@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/05/03 14:27:53 by cherrero          #+#    #+#              #
#    Updated: 2023/06/08 20:40:30 by cherrero         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
sys.tracebacklimit = 0

class CsvReader():
	def __init__(self, filename=None, sep=", ", header=False, skip_top=0, skip_bottom=0):
		''' Constructor of the class '''
		self.filename = filename
		self.sep = sep
		self.header = header
		self.skip_top = skip_top
		self.skip_bottom = skip_bottom
		self.file = None
		self.data = []
		self.__data = None
		self.__header = None
		
	def __enter__(self):
		''' Opens the file and reads && check its content '''
		try:
			self.file = open(self.filename, "r")
		except FileNotFoundError:
			return None
		for line in self.file:
			self.data.append(list(map(str.strip, line.split(self.sep))))
		if all(len(elem) == len(self.data[0]) for elem in self.data):
			return self
		else:
			return None

	def __exit__(self, exc_type, exc_val, exc_tb):
		''' Closes the file '''
		try:
			self.file.close()
		except:
			return None
		
	def getdata(self):
		""" Retrieves the data/records from skip_top to skip bottom.
		Return:
			nested list (list(list, list, ...)) representing the data.
		"""
		if self.header:
			self.skip_top += 1
		return self.data[self.skip_top : len(self.data) - self.skip_bottom]

	def getheader(self):
		""" Retrieves the header from csv file.
		Returns:
			list: representing the data (when self.header is True).
			None: (when self.header is False).
		"""
		if self.header == True:
			return self.data[0]
		else:
			return None
