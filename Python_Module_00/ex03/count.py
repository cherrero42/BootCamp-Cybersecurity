# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    count.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cherrero <cherrero@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/11 16:36:16 by cherrero          #+#    #+#              #
#    Updated: 2023/04/13 17:24:55 by cherrero         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
import string

def text_analyzer(arg=""):
    '''
        Create a function called text_analyzer that takes a single string argument and displays
        the sums of its upper-case characters, lower-case characters, punctuation characters and spaces.
    '''
    count_upper, count_lower, count_space, count_spcal = 0, 0, 0, 0
    if not isinstance(arg, str):
        exit("AssertionError: argument is not a string.")
    if (len(arg) == 0):
        print("What is the text to analyze?")
        print(">> ", end="")
        arg = input()
    for i in range(len(arg)):
        if arg[i].isupper():
            count_upper += 1
        elif arg[i].islower():
            count_lower += 1
        elif arg[i] in string.punctuation:
            count_spcal += 1
        elif arg[i].isspace():
            count_space += 1
    print(f"The text contains {len(arg)} character(s):")
    print(f"- {count_upper} upper letter(s)")
    print(f"- {count_lower} lower letter(s)")
    print(f"- {count_spcal} punctuation mark(s)")
    print(f"- {count_space} space(s)")

if __name__ == '__main__':
    
    if len(sys.argv) > 2:
        print("AssertionError: more than one argument are provided.")
    else:
        text_analyzer(*sys.argv[1:])