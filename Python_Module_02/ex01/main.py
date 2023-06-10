#!/usr/bin/env python
# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cherrero <cherrero@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/05/01 14:27:53 by cherrero          #+#    #+#              #
#    Updated: 2023/06/08 15:15:19 by cherrero         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

def what_are_the_vars(*args, **kwargs):
	obj = ObjectC()
	for x, varg in enumerate(args):
		setattr(obj, f"var_{x}", varg)
	for x, varg in kwargs.items():
		if hasattr(obj, x):
			return None
		setattr(obj, x, varg)
	return obj

class ObjectC(object):
	def __init__(self):
		# ... Your code here ...
		pass

def doom_printer(obj):
		if obj is None:
				print("ERROR")
				print("end")
				return
		for attr in dir(obj):
				if attr[0] != "_":
						value = getattr(obj, attr)
						print("{}: {}".format(attr, value))
		print("end")

# if __name__ == "__main__":
# 	obj = what_are_the_vars(7)
# 	doom_printer(obj)
# 	obj = what_are_the_vars(None)
# 	doom_printer(obj)
# 	obj = what_are_the_vars()
# 	doom_printer(obj)
# 	obj = what_are_the_vars(lambda x: x, function=what_are_the_vars)
# 	doom_printer(obj)
# 	obj = what_are_the_vars(3, var_0=2)
# 	doom_printer(obj)
# 	obj = what_are_the_vars("ft_lol", "Hi")
# 	doom_printer(obj)
# 	obj = what_are_the_vars()
# 	doom_printer(obj)
# 	obj = what_are_the_vars(12, "Yes", [0, 0, 0], a=10, hello="world")
# 	doom_printer(obj)
# 	obj = what_are_the_vars(42, a=10, var_0="world")
# 	doom_printer(obj)
# 	obj = what_are_the_vars(42, "Yes", a=10, var_2="world")
# 	doom_printer(obj)