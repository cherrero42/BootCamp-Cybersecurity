# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    kata02.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cherrero <cherrero@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/11 16:37:26 by cherrero          #+#    #+#              #
#    Updated: 2023/04/13 12:55:49 by cherrero         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

kata = (2019, 9, 25, 3, 30)

if __name__ == '__main__':
	
	print("{1:02d}/{2:02d}/{0:04d} {3:02d}:{4:02d}".format(*kata))