# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    guess.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cherrero <cherrero@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/11 16:39:06 by cherrero          #+#    #+#              #
#    Updated: 2023/04/13 16:35:24 by cherrero         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import random

global exit
exit = False

def eval_choice(option):
        global exit
        msj_42 = ""
        if choice == 42:
            msj_42 = "The answer to the ultimate question of life, the universe and everything is 42.\n"
        if choice < 1 or choice > 99:
            print("Please, you have to enter a number between 1 and 99.")
        elif choice < guess:
            print("Too low!")
        elif choice > guess:
            print("Too high!")
        elif choice == guess and iter == 1:
            print(msj_42 + "Congratulations! You got it on your first try!!")
            exit = True
        elif choice == guess and iter > 1:
            print(msj_42 + "Congratulations, you've got it!")
            print(f"You won in {iter} attempts!")
            exit = True
 
if __name__ == '__main__':
    
    print("This is an interactive guessing game!!\nYou have to enter a number between 1 and 99 to find out the secret number.\nType 'exit' to end the game.\nGood luck!")
    guess = random.randint(1, 99)
    iter = 1
    
    while not exit:
        choice = input("What's your guess between 1 and 99?\n>> ")
        if choice == 'exit':
            print("Goodbye!")
            break
        try:
            choice = int(choice)
        except ValueError:
            print("Moooc... write a number.")
            iter += 1
            continue
        eval_choice(choice)
        iter += 1
