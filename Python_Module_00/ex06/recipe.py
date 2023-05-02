# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    recipe.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cherrero <cherrero@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/11 16:38:06 by cherrero          #+#    #+#              #
#    Updated: 2023/04/13 21:03:43 by cherrero         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #







# anadir otro elemento
cookbook = { 'sandwich': {'ingredients': ("ham", "bread", "cheese", "tomatoes"), 'meal': "lunch", 'prep_time': 10, },
    'cake': {'ingredients': ("flour", "sugar", "eggs"), 'meal': "desert", 'prep_time': 60, },
    'salad': { 'ingredients': ("avocado", "arugula", "tomatoes", "spinach"), 'meal': 'lunch', 'prep_time': 15, }, }

def cook_functions(f):
    ops = {
        1: prompt_add_recipe,
        2: delete_recipe,
        3: print_one_recipe,
        4: print_all_recipes,
        5: exit,
        6: wrong_choice,
        7: print_instructions,
    }
    return ops[f]

def print_instructions(new_line=''):
    print("""{}Welcome to the Python Cookbook !
List of available option:
\t1: Add a recipe
\t2: Delete a recipe
\t3: Print a recipe
\t4: Print the cookbook
\t5: Quit

Please select an option:
""".format(new_line))


def print_one_recipe(recipe=""):
    recipe = recipe_prompt(
        recipe=recipe,
        message="get its details:")
    if not recipe:
        return
    info = cookbook[recipe]
    print("""Recipe for {}:
Ingredients list: [{}]
To be eaten for {}.
Takes {} minutes of cooking.""".format(
        recipe,
        ', '.join("'{}'".format(w) for w in info['ingredients']),
        info['meal'],
        info['prep_time']))

def print_all_recipes():
    for recipe in cookbook:
        print_one_recipe(recipe)


def delete_recipe(recipe=''):
    recipe = recipe_prompt(
        recipe=recipe,
        message="delete it:")
    if not recipe:
        return
    del cookbook[recipe]


def add_recipe(name, ingredients, meal, prep_time):
    cookbook[name] = {
        'ingredients': ingredients,
        'meal': meal,
        'prep_time': prep_time,
    }

if __name__ == '__main__':
    choice = 0
    while (choice != 5):
        cook_functions(choice)()
        choice = get_choice(choice)
''''



def new_recipe_inputs(label="Your answer", restrict=False):
    value = input()
    while not value:
        print("%s can't be empty. [always 5 to 'Quit'" % label)
        value = input()

    while restrict:
        try:
            value = int(value)
            restrict = False
        except Exception:
            print("Cook time should be a number (int) of minutes.")
            value = input()

    if value == '5':
        print("CANCELED")
        return
    return value


def prompt_add_recipe():
    print("Add a new recipe to the cookbook")
    print("Name:")
    name = new_recipe_inputs("Recipe name")
    if not name:
        return
    print("Ingredients (separate by spaces: example:'riz lait banane bacon'):")
    ingredients = new_recipe_inputs(
        "Ingredient list").replace(
            "'", "").replace(",", " ").split()
    if not ingredients:
        return
    print("Meal type:")
    meal = new_recipe_inputs("Meal type")
    if not meal:
        return
    print("Preparation time:")
    prep_time = new_recipe_inputs("Preparation time", restrict=True)
    if not prep_time:
        return
    add_recipe(name, ingredients, meal, prep_time)




def recipe_prompt(recipe='', message=''):
    while recipe not in cookbook:
        print("Please enter the recipe's name to %s" % message)
        recipe = input()
        if recipe == '5':
            return
    return recipe






def wrong_choice():
    print("""This option does not exist, please type the corresponding number.
To exit, enter 5.""")






def get_choice(choice):
    if choice < 5:
        print_instructions(new_line='\n')
    choice = input()
    try:
        choice = int(choice)
    except Exception:
        choice = 6
    if choice < 0 or choice > 5:
        return 6
    return choice



'''