#!/usr/bin/env python
# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_map.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cherrero <cherrero@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/05/01 14:27:53 by cherrero          #+#    #+#              #
#    Updated: 2023/06/07 12:03:42 by cherrero         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys

def ft_map(function_to_apply, iterable):
    """Map the function to all elements of the iterable.
        Args:
            function_to_apply: a function taking an iterable.
            iterable: an iterable object (list, tuple, iterator).
        Return:
            An iterable.
            None if the iterable can not be used by the function.
     """
    try:
        return (function_to_apply(item) for item in iterable)
    except TypeError:
        return None

