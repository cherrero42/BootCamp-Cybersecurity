#!/usr/bin/env python
# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    book.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cherrero <cherrero@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/05/01 14:27:53 by cherrero          #+#    #+#              #
#    Updated: 2023/05/02 12:30:46 by cherrero         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from datetime import datetime
from recipe import Recipe

class Book:
    '''*** my book of recipes class ***'''
    def __init__(self, name=str()):
        self.name = name
        self.last_update = datetime.now()
        self.creation_date = datetime.now()
        self.recipes_list = {"starter": [], "lunch": [], "dessert": []}


    def add_recipe(self, recipe):
        '''*** add a recipe to the book ***'''
        self.recipe_list[recipe.recipe_type].append(recipe)
        self.last_update = datetime.now()

    def __str__(self):
        '''*** string representation of the class ***'''
        starter_recipes = "\n".join([recipe.name for recipe in self.recipe_list["starter"]])
        lunch_recipes = "\n".join([recipe.name for recipe in self.recipe_list["lunch"]])
        dessert_recipes = "\n".join([recipe.name for recipe in self.recipe_list["dessert"]])

        return f"{self.name}\n" \
               f"Creation date: {self.creation_date}\n" \
               f"Last update: {self.last_update}\n" \
               f"\n" \
               f"Starter recipes:\n{starter_recipes}\n" \
               f"\n" \
               f"Lunch recipes:\n{lunch_recipes}\n" \
               f"\n" \
               f"Dessert recipes:\n{dessert_recipes}"

    def get_recipe_by_name(self, name):
        """Prints a recipe with the name \texttt{name} and returns the instance"""
        for recipe_type in self.recipes_list.values():
            for recipe in recipe_type:
                if recipe.name == name:
                    print(recipe)
                    return recipe
        print(f"No recipe found with the name {name}")
        return None
    
    def get_recipes_by_types(self, recipe_type):
        """Get all recipe names for a given recipe_type """
        if recipe_type not in self.recipes_list.keys():
            print(f"{recipe_type} is not a valid recipe type")
            return None
        recipe_names = [recipe.name for recipe in self.recipes_list[recipe_type]]
        print(f"All recipe names for {recipe_type}: {recipe_names}")
        return recipe_names

    def add_recipe(self, recipe):
        """Add a recipe to the book and update last_update"""
        if not isinstance(recipe, Recipe):
            print("Invalid recipe")
            return None
        self.recipes_list[recipe.recipe_type].append(recipe)
        self.last_update = datetime.now()
        print(f"Added recipe: {recipe.name}")

