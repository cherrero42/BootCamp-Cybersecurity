#!/usr/bin/env python
# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_reduce.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cherrero <cherrero@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/05/01 14:27:53 by cherrero          #+#    #+#              #
#    Updated: 2023/06/07 12:04:06 by cherrero         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

def ft_reduce(function_to_apply, iterable):
    """Apply function of two arguments cumulatively.
    Args:
        function_to_apply: a function taking an iterable.
        iterable: an iterable object (list, tuple, iterator).
    Return:
        A value, of same type of elements in the iterable parameter.
        None if the iterable can not be used by the function.
    """
    if len(iterable) == 0:
        return ("ERROR")
    a = iterable[0]
    for i in iterable[1:]:
        a = function_to_apply(a, i)
    return(a)