#!/usr/bin/env python
# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    logger.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cherrero <cherrero@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/05/04 14:27:53 by cherrero          #+#    #+#              #
#    Updated: 2023/06/08 18:39:05 by cherrero         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import time
from random import randint
import os

def log(function):
    def wrapper(*args, **kwargs):
        user_name = os.environ["USER"]
        start = time.perf_counter()
        run = function(*args, **kwargs)
        total = time.perf_counter() - start
        if (total < 1.0):
            total = f"[ exec-time {(total * 1000):.3f} ms ]"
        else:
            total = f"[ exec-time {(total):.3f} s ]"
        task = function.__name__.replace("_", " ").title()
        log = (f"({user_name})Running: {task: <19}{total}\n")
        with open('machine.log', 'a') as file:
            file.write(log)
        return run
    return wrapper

class CoffeeMachine():
    water_level = 100
    @log
    def start_machine(self):
        if self.water_level > 20:
            return True
        else:
            print("Please add water!")
            return False

    @log
    def boil_water(self):
        return "boiling..."

    @log
    def make_coffee(self):
        if self.start_machine():
            for _ in range(20):
                time.sleep(0.1)
                self.water_level -= 1
            print(self.boil_water())
            print("Coffee is ready!")
    @log
    def add_water(self, water_level):
        time.sleep(randint(1, 5))
        self.water_level += water_level
        print("Blub blub blub...")

if __name__ == "__main__":
        machine = CoffeeMachine()
        for i in range(0, 5):
            machine.make_coffee()

        machine.make_coffee()
        machine.add_water(70)