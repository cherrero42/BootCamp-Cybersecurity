#!/usr/bin/env python
# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    game.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cherrero <cherrero@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/05/01 14:27:53 by cherrero          #+#    #+#              #
#    Updated: 2023/05/02 23:17:36 by cherrero         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

class GotCharacter:
	''' Game of Thrones character'''
	def __init__(self, first_name, is_alive=True):
		self.first_name = first_name
		self.is_alive = is_alive

class Stark(GotCharacter):
	'''sub-class of GotCharacter'''
	def __init__(self, first_name=None, is_alive=True):
		super().__init__(first_name=first_name, is_alive=is_alive)
		self.family_name = "Stark"
		self.house_words = "Winter is Coming"

	def print_house_words(self):
		'''prints to screen the house words'''
		print(self.house_words)
		
	def die(self):
		'''kills the character'''
		self.is_alive = False
