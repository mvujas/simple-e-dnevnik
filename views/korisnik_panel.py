from abc import ABC, abstractmethod
from utils import clear_screen

class KorisnikPanel(ABC):
	# ACTION_DICTIONARY should be a list of (action name, action callback) pairs
	# action callback is function that accepts instance of object Korisnik
	ACTION_DICTIONARY = []

	__STARTING_ACTION_NUMBER = 1

	def __init__(self, korisnik):
		self.korisnik = korisnik
		self.loop()

	def loop(self):
		while True:
			clear_screen()
			print(self.panel_heading)
			print()
			print(self.user_identity)
			print()
			print(' _____ Akcije _____ ')
			for counter, action in enumerate(self.ACTION_DICTIONARY, self.__STARTING_ACTION_NUMBER):
				print(' {}) {}'.format(counter, action[0]))
			print(' X) Odjavi se ')
			print()
			action = input('Izaberite akciju: ').strip()
			if action.upper() == 'X':
				return
			self.__handle_action(action)

	@property
	@abstractmethod
	def panel_heading(self):
		pass

	@property
	@abstractmethod
	def user_identity(self):
		pass 

	def __handle_action(self, action):
		size = len(self.ACTION_DICTIONARY)
		if not action.isdigit():
			print('Nevalidna vrednost akcije')
		else:
			action_num = int(action) - self.__STARTING_ACTION_NUMBER
			if action_num < 0 or action_num >= size: 
				print('Nevalidna vrednost akcije')
			else:
				self.ACTION_DICTIONARY[action_num][1](self.korisnik)
		input('Kliknite ENTER za povratak na panel...')