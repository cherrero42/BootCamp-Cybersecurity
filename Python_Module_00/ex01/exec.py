# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    exec.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cherrero <cherrero@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/11 16:35:35 by cherrero          #+#    #+#              #
#    Updated: 2023/04/11 23:05:37 by cherrero         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys

args = sys.argv[1:]
# if not args:
#     print("Please give me args")
if __name__ == '__main__':
     if len(sys.argv) > 2:
        print(''.join(arg.swapcase() for arg in ' '.join(args).strip()[::-1]))
