# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    operations.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cherrero <cherrero@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/11 16:36:33 by cherrero          #+#    #+#              #
#    Updated: 2023/04/13 18:22:22 by cherrero         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("AssertionError: need two arguments to operate. Use with two integer args.")
    elif len(sys.argv) > 3:
        print("AssertionError: more than two arguments are provided. Use with two integer args.")
    elif len(sys.argv) < 3:
        print("AssertionError: less than two arguments are provided. Use with two integer args.")
    elif not sys.argv[1].lstrip('-').isdigit() or not sys.argv[2].lstrip('-').isdigit():
        print("AssertionError: arguments are not integer. Use with two integer args.")
    else:
        a = int(sys.argv[1])
        b = int(sys.argv[2])
        print("Sum:\t\t%d" %(a + b))
        print("Difference:\t%d" %(a - b))
        print("Product:\t%d" %(a * b))
        print("Quotient:\t", end="")
        print(f"{a / b}" if (b != 0) else "ERROR (division by zero)")
        print("Remainder:\t", end="")
        print(f"{a % b}" if (b != 0) else "ERROR (modulo by zero)")
