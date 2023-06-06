#!/usr/bin/env python
# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    eval.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cherrero <cherrero@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/05/01 14:27:53 by cherrero          #+#    #+#              #
#    Updated: 2023/05/04 22:52:16 by cherrero         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

class Evaluator:
	@staticmethod
	def zip_evaluate(coefs, words):
		'''zip_evaluate'''
		if len(coefs) != len(words):
			return -1
		return sum(coef * len(word) for coef, word in zip(coefs, words))

	@staticmethod
	def enumerate_evaluate(coefs, words):
		'''enumerate_evaluate'''
		if len(coefs) != len(words):
			return -1
		return sum(coefs[i] * len(words[i]) for i, _ in enumerate(words))
