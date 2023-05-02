# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    loading.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cherrero <cherrero@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/11 16:39:24 by cherrero          #+#    #+#              #
#    Updated: 2023/04/30 10:23:43 by cherrero         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import time
 
def ft_progress(lst):
    eta, delta, leng = 0, 0, 30
    lst_size, time_on = len(lst), time.time()
    wh = lst_size / 18
    for i, pos in enumerate(lst, 1):
        ratio = i / lst_size
        now, adv, bar = time.time(), ratio * 100, ("#" * int(ratio * (leng))) 
        elap_time = now - time_on
        if delta != 0:
            eta = (lst_size - i) * delta
        print("\rETA: %.2fs [%3d%%][%-*s] %d/%d | elapsed time %.2fs" %(eta, adv, leng, bar, i, lst_size, elap_time), end="")
        yield (pos)
        if (delta == 0) or (i % wh) == 0:
            delta = time.time() - now

def main():
    lst = range(1000)
    ret = 0
    for elem in ft_progress(lst):
        ret += (elem + 3) % 5
        time.sleep(0.01)
    print()
    print(ret)

def main_2():
    listy = range(3333)
    ret = 0
    for elem in ft_progress(listy):
        ret += elem
        time.sleep(0.005)
    print()
    print(ret)

if __name__ == "__main__":
    main()