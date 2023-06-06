#!/usr/bin/env python
# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    vector.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cherrero <cherrero@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/05/01 14:27:53 by cherrero          #+#    #+#              #
#    Updated: 2023/05/03 00:15:19 by cherrero         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

def is_range(tpl):
	if not isinstance(tpl, tuple) or len(tpl) != 2:
		return False
	if not isinstance(tpl[0], int) and isinstance(tpl[1], int) and tpl[0] < tpl[1]:
		return False
	return True

class Vector:
	def __init__(self, values):
		self.values = []
		try:
			if isinstance(values, list):
				print("list")
				# column vector
				self.values = values
				self.shape = (1, len(values))
			elif isinstance(values, int):
				print("int")
				if values < 0:
					print("int < 0: Invalid values for Vector")
					return
				print("int")
				self.shape = (values, 1)
				for i in range(values):
					self.values.append([float(i)])
			elif isinstance(values, (int, float)):
				print("int or float")
				# row vector
				self.values = values
				self.shape = (values, 1)
				for i in range(values):
					self.values.append([float(i)])
			elif is_range(values):
				print("range")
				self.shape = (values[1] - values[0], 1)
				for i in range(values[0], values[1]):
					self.values.append([float(i)])
			else:
				raise TypeError("Invalid input type")
		except:
			raise ValueError("Invalid input for values attribute")

	def __str__(self):
		'''Prints the vector'''
		return str(self.values)

	def dot(self, other):
		'''Computes the dot product of two vectors'''
		if self.shape != other.shape:
			raise ValueError("Dot product is not possible")
		if self.shape != other.shape:
			raise ValueError("Vectors must be of the same shape")
		result = 0
		for i in range(self.shape[0]):
			for j in range(self.shape[1]):
				print(i,j)
				result += self.values[i][j] * other.values[i][j]
		return result

	def T(self):
		'''Returns the transpose of the vector'''
		if self.shape == (1,1):
			return self
		if self.shape[0] == 1:
			return Vector([[x] for x in self.values[0]])
		else:
			return Vector(self.values[::])

	def __add__(self, other):
		'''Adds two vectors'''
		if self.shape != other.shape:
			raise ValueError("Shapes of vectors do not match.")
		new_values = []
		for i in range(self.shape[0]):
			new_row = []
			for j in range(self.shape[1]):
				new_row.append(self.values[i][j] + other.values[i][j])
			new_values.append(new_row)
		return Vector(new_values)
	
	def __sub__(self, other):
		'''Subtracts two vectors'''
		if self.shape != other.shape:
			raise ValueError("Shapes of vectors do not match.")
		new_values = []
		for i in range(self.shape[0]):
			new_row = []
			for j in range(self.shape[1]):
				new_row.append(self.values[i][j] - other.values[i][j])
			new_values.append(new_row)
		return Vector(new_values)

	def __mul__(self, other):
		'''Multiplies a vector by a scalar'''
		if isinstance(other, (int, float)):
			new_values = []
			for i in range(self.shape[0]):
				new_row = []
				for j in range(self.shape[1]):
					new_row.append(self.values[i][j] * other)
				new_values.append(new_row)
			return Vector(new_values)
		else:
			raise TypeError("Invalid type for multiplication.")

	def __rmul__(self, other):
		'''Multiplies a vector by a scalar'''
		return self.__mul__(other)

	def __truediv__(self, other):
		'''Divides a vector by a scalar'''
		if isinstance(other, (int, float)):
			new_values = []
			for i in range(self.shape[0]):
				new_row = []
				for j in range(self.shape[1]):
					new_row.append(self.values[i][j] / other)
				new_values.append(new_row)
			return Vector(new_values)
		else:
			raise TypeError("Invalid type for division.")

	def __rtruediv__(self, other):
		'''Divides a vector by a scalar'''
		raise ArithmeticError("Division of a vector by a scalar is not supported in reverse order.")
