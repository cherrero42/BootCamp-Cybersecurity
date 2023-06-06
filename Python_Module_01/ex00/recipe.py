#!/usr/bin/env python
# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    recipe.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cherrero <cherrero@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/05/01 14:27:53 by cherrero          #+#    #+#              #
#    Updated: 2023/05/02 12:30:46 by cherrero         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

class Recipe:
	'''*** my recipes class ***'''
	def __init__(self, name=str(), cooking_lvl=int(), cooking_time=int(),
			ingredients=list(), description=str(), recipe_type=str()):

		if not name or not cooking_lvl or not cooking_time or not ingredients or not description or not recipe_type:
			print("Error: any args should not be empty.")
			return
		if not isinstance(name, str) or not isinstance(description, str) or not isinstance(recipe_type, str):
			print("Error: name, description and recipe_type should be a string.")
			return

		# Check for input errors

		if not isinstance(name, str):
			print("Error: name should be a string.")
			return
		if not isinstance(cooking_lvl, int) or not (1 <= cooking_lvl <= 5):
			print("Error: cooking_lvl should be an integer between 1 and 5.")
			return
		if not isinstance(cooking_time, int) or cooking_time < 0:
			print("Error: cooking_time should be a non-negative integer.")
			return
		if not isinstance(ingredients, list):
			print("Error: ingredients should be a list of strings.")
			return
		for ingredient in ingredients:
			if not isinstance(ingredient, str):
				print("Error: each ingredient should be a string.")
				return
		if not isinstance(description, str):
			print("Error: description should be a string.")
			return
		if recipe_type not in ["starter", "lunch", "dessert"]:
			print("Error: recipe_type should be 'starter', 'lunch', or 'dessert'.")
			return
	
		self.name = str(name)
		self.cooking_lvl = cooking_lvl
		self.cooking_time = cooking_time
		self.ingredients = ingredients
		self.description = str(description)
		self.recipe_type = str(recipe_type)
		print(name, "created")

		
	def __str__(self):
		"""recipe info"""
		return f"{self.name} ({self.recipe_type})\nDifficulty: {self.cooking_lvl}/5\nTime: {self.cooking_time} min\nIngredients: {', '.join(self.ingredients)}\nDescription: {self.description}"
	
	
