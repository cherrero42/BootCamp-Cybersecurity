# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    kata00.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cherrero <cherrero@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/11 16:36:57 by cherrero          #+#    #+#              #
#    Updated: 2023/04/13 12:54:29 by cherrero         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

kata = (19,21,32)

if __name__ == '__main__':

    if len(kata) > 0:
        print("The {} number(s) are: {}".format(len(kata), ", ".join(str(element) for element in kata)))
    else:
        print("No data in the tuple.")
