#!/usr/bin/env python
# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    whois.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cherrero <cherrero@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/11 16:35:58 by cherrero          #+#    #+#              #
#    Updated: 2023/04/11 23:04:59 by cherrero         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys

def isNumeric(s):
    return s.isdigit()

if __name__ == '__main__':
    if len(sys.argv) > 2:
        print("AssertionError: more than one argument are provided.")
    elif len(sys.argv) == 2:
        if not isNumeric(sys.argv[1]):
            print("AssertionError: argument is not an integer.")
        elif int(sys.argv[1]) == 0:
            print("I'm Zero.")
        elif int(sys.argv[1]) % 2 == 0:
            print("I'm Even.")
        elif int(sys.argv[1]) % 2 == 1:
            print("I'm Odd.")
