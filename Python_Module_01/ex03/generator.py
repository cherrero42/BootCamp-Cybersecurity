#!/usr/bin/env python
# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    generator.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cherrero <cherrero@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/05/01 14:27:53 by cherrero          #+#    #+#              #
#    Updated: 2023/05/02 23:17:54 by cherrero         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import random

def generator(text, sep, option=None):
	'''Option is an optional arg, sep is mandatory'''
	if not isinstance(text, str):
		print("ERROR")
		return
	if option and option not in ["shuffle", "unique", "ordered"]:
		print("ERROR")
		return
	words = text.split(sep)
	if option == 'shuffle':
		words = shuffle_list(words)
	elif option == 'unique':
		words = list(set(words))
	elif option == 'ordered':
		words = sorted(words)
	for word in words:
		yield word

def shuffle_list(lst):
    '''Fisher-Yates algorithm to shuffle list without using random.shuffle'''
    shuffled_lst = lst[:]
    for i in range(len(shuffled_lst) - 1, 0, -1):
        j = random.randint(0, i)
        shuffled_lst[i], shuffled_lst[j] = shuffled_lst[j], shuffled_lst[i]
    return shuffled_lst
