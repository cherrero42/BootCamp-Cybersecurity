#!/usr/bin/env python
# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_filter.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cherrero <cherrero@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/05/01 14:27:53 by cherrero          #+#    #+#              #
#    Updated: 2023/06/07 12:43:23 by cherrero         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

def ft_filter(function_to_apply, iterable):
	"""Filter the result of function apply to all elements of the iterable.
	Args:
		function_to_apply: a function taking an iterable.
		iterable: an iterable object (list, tuple, iterator).
	Return:
			An iterable.
		None if the iterable can not be used by the function.
	"""
	for i in iterable:
		if function_to_apply(i):
			yield(i)

