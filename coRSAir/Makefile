# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cherrero <cherrero@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/05/06 22:14:31 by cherrero          #+#    #+#              #
#    Updated: 2023/05/30 18:34:35 by cherrero         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


NAME    = corsair
CFLAGS  = -Wall -Wextra -lm -Wno-deprecated-declarations

INC = /Users/cherrero/.brew/opt/openssl@3/include
LIB = /Users/cherrero/.brew/opt/openssl@3/lib

CC = gcc

# COLORS
GREEN = \033[0;32m
RED = \033[0;31m
RESET = \033[0m

all: ${NAME}
	@echo "$(NAME): $(GREEN)$(NAME) created$(RESET)"

SOURCES = corsair.c
OBJECTS = corsair.o

${NAME}: corsair.o
	${CC} corsair.o  -L$(LIB) -lssl -lcrypto -o corsair
	@echo "$(NAME): $(GREEN)Creating $(NAME)...$(RESET)"

corsair.o: corsair.c
	${CC} -c $(SOURCES) $(CFLAGS) -I$(INC) -o corsair.o

clean:
	@rm -rf corsair.o
	@echo "$(RED)$(OBJECTS)$ cleaned$(RESET)"

fclean: clean
	@rm -f $(NAME)
	@echo "$(NAME): $(RED)$(NAME) cleaned$(RESET)"

re: fclean all

test: all
	./corsair ./sample/60.pem ./sample/97.pem ./sample/60.bin

.PHONY: all clean fclean re test
