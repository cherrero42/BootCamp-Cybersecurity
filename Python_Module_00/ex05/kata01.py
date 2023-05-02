# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    kata01.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cherrero <cherrero@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/11 16:37:09 by cherrero          #+#    #+#              #
#    Updated: 2023/04/13 12:43:23 by cherrero         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

kata = {
'Python': 'Guido van Rossum',
'Ruby': 'Yukihiro Matsumoto',
'PHP': 'Rasmus Lerdorf',
}

if __name__ == '__main__':
	
	if len(kata) > 0:
		for x in kata:
			print(x + " was created by " + kata[x])
	else:
		print("No data in the dictionary.")