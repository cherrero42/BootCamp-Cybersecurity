#!/usr/bin/env python
# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    the_bank.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cherrero <cherrero@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/05/01 14:27:53 by cherrero          #+#    #+#              #
#    Updated: 2023/05/04 23:08:36 by cherrero         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

class Account(object):
	ID_COUNT = 1
	def __init__(self, name, **kwargs):
		'''class that represents a bank account'''
		self.__dict__.update(kwargs)
		self.id = self.ID_COUNT
		Account.ID_COUNT += 1
		self.name = name
		self.__args = len(kwargs) % 2 != 0
		if not hasattr(self, 'value'):
			self.value = 0
		if self.value < 0:
			raise AttributeError("Attribute value cannot be negative.")
		if not isinstance(self.name, str):
			raise AttributeError("Attribute name must be a str object.")

	def transfer(self, amount):
		"""Transfer amount to this account"""
		self.value += amount
	

	def _is_corrupted(self):
		"""Helper method to check if an account is corrupted"""
		if not self.__args:
			return True
		if any([elem.startswith('b') for elem in dir(self)]):
			return True
		if all([not elem.startswith(('zip', 'addr')) for elem in dir(self)]):
			return True
		if not isinstance(self.name, str) or not isinstance(self.id, int) or not isinstance(self.value, (int, float)):
			return True
		if not all(elem in dir(self) for elem in ('name', 'id', 'value')):
			return True
		return False

	def _str_(self):
		return "Account name: %s, value: %s" % (self.name, self.value)
	
class Bank(object):
	"""The bank"""
	def __init__(self):
		'''class that represents a bank'''
		self.accounts = []
		
	def add(self, new_account):
		""" Add new_account in the Bank
		@new_account: Account() new account to append
		@return True if success, False if an error occured
		"""
		if not isinstance(new_account, Account):
			return False
		for account in self.accounts:
			if account.name == new_account.name:
				return False
		self.accounts.append(new_account)
		return True
	
	def transfer(self, origin, dest, amount):
		"""" Perform the fund transfer
		@origin: str(name) of the first account
		@dest: str(name) of the destination account
		@amount: float(amount) amount to transfer
		@return True if success, False if an error occured
		"""
		origin_account = self._find_account(origin)
		dest_account = self._find_account(dest)
		
		if origin_account is None or dest_account is None:
			return False
		
		if amount < 0 or amount > origin_account.value:
			return False
		
		origin_account.transfer(-amount)
		dest_account.transfer(amount)
		return True
	
	def fix_account(self, name):
		""" fix account associated to name if corrupted
		@name: str(name) of the account
		@return True if success, False if an error occured
		"""
		if not isinstance(name, str):
			return False
		account = self._find_account(name)
		
		if account is None:
			return False
		if not account._is_corrupted():
			return True
		if not any(attr.startswith(('zip', 'addr')) for attr in dir(account)):
			account.zip = None
		b_attr = [a for a in dir(account) if a.startswith('b')]
		for attr in b_attr:
			account.__dict__[f'_{attr}'] = account.__dict__.pop(attr)
		return not account._is_corrupted()
	
	def _find_account(self, name):
		"""Helper method to find an account object by name"""
		for account in self.accounts:
			if account.name == name:
				return account
		return None
	
