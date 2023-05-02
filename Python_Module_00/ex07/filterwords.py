# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    filterwords.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cherrero <cherrero@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/11 16:38:28 by cherrero          #+#    #+#              #
#    Updated: 2023/04/13 10:23:08 by cherrero         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
import string

if __name__ == '__main__':
    
    if (len(sys.argv) != 3):
        exit("ERROR")
    try:
        words = str(sys.argv[1])
        number = int(sys.argv[2])
    except ValueError:
        exit("ERROR")
    
    words_clean = sys.argv[1].translate(str.maketrans("", "", string.punctuation))

    words_split = words_clean.split()

    print([word for word in words_split if len(word) > number])




