from utils import clear_screen
from abc import ABC

class EntityView(ABC):
	heading = ''
	entity_info_function = lambda entity: ''
	ACTION_DICTIONARY = []

	def __init__(self, entity_load_func):
		self.entity_load_funcion = entity_load_func
		self.ACTION_DICTIONARY = self.ACTION_DICTIONARY[:]
		self.loop()

	def loop(self):
		while True:
			clear_screen()
			entity = self.entity_load_funcion()
			if entity is None:
				print('Objekat se ne moze ucitati')
				input()
			entity_info = self.entity_info_function.__func__(entity)
			print(f'''\
{self.heading}

{entity_info}
__________ Akcije __________
''')
			for counter, akcija in enumerate(self.ACTION_DICTIONARY):
				print(f' {counter + 1}) {akcija[0]}')
			print(' X) Vrati se nazad')
			print('____________________________')
			akcija = input('Akcija: ').strip().upper()
			if akcija == 'X':
				return
			elif akcija.isdigit():
				self.process_action(entity, int(akcija) - 1)
			else:
				print(' * Nevalidna vrednost akcije')
				input()

	def process_action(self, entity, akcija_num):
		if akcija_num < 0 or akcija_num >= len(self.ACTION_DICTIONARY):
			print(' * Nevalidna vrednost akcije')
			input()
			return
		self.ACTION_DICTIONARY[akcija_num][1](entity)