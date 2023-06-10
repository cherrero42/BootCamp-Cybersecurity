#!/usr/bin/env python
# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    TinyStatistician.py                                :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cherrero <cherrero@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/05/03 14:27:53 by cherrero          #+#    #+#              #
#    Updated: 2023/06/09 22:47:50 by cherrero         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

class TinyStatistician:
    def mean(self, x) -> float:
        if not isinstance(x, list) or not x:
            return None
        size = len(x)
        if size == 0:
            return None
        return sum(x) / size

    def median(self, x: list) -> float:
        if not isinstance(x, list) or not x:
            return None
        size = len(x)
        if size == 0:
            return None
        return sorted(x)[size // 2]

    def quartiles(self, x):
        if not isinstance(x, list) or not x:
            return None
        if len(x) == 0:
            return None
        
        sorted_x = sorted(x)
        size = len(sorted_x)
        
        q1_index = (size) // 4
        q3_index = 3 * ((size) // 4)
        
        q1 = sorted_x[q1_index]
        q3 = sorted_x[q3_index]
        
        return q1, q3

    def var(self, x) -> float:
        if not isinstance(x, list) or not x:
            return None
        size = len(x)
        if size == 0:
            return None
        return sum(map(lambda n: pow(n - self.mean(x), 2), x)) / size

    def std(self, x) -> float:
        if not isinstance(x, list) or not x:
            return None
        return self.var(x) ** 0.5
