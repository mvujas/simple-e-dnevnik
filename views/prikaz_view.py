from prettytable import PrettyTable
from utils import clear_screen
from abc import ABC, abstractmethod

class ListAllView(ABC):
	list_sortings = {}
	list_heading = ''
	table_mapping = [] # table_mapping should be list of tupples (column heading, column mapping[entry -> string])
	akcije = []
	prikaz_pojedinacnog = None

	def __init__(self):
		assert len(self.table_mapping) > 0
		self.__current_sorting = None
		if self.__current_sorting is None and 'default' in self.list_sortings:
			self.__current_sorting = 'default'
		self.akcije = self.akcije[:]
		if self.prikaz_pojedinacnog is not None:
			self.akcije.insert(0, ('Prikaz pojedinacnog', self.prikaz_pojedinacnog_unos))
		if len(self.list_sortings) > 0:
			self.akcije.insert(0, ('Izmeni sortiranje', self.promena_sortiranja))
		self.loop()
		self.list_entries_dict = None

	@abstractmethod
	def list_supplier(self): # should return dictionary where keys are primary keys and values objects
		pass

	def loop(self):
		while True:
			clear_screen()
			print(self.list_heading)

			self.list_entries_dict = self.list_supplier()
			if self.list_entries_dict is None:
				print('Doslo je do greske prilikom ucitavanja podataka!')
				input()
				return
			list_entries = list(self.list_entries_dict.values())
			if self.__current_sorting is not None:
				sorting = self.list_sortings[self.__current_sorting]
				sorting_key = sorting[0]
				sorting_reverse = sorting[1]
				list_entries.sort(key=sorting_key, reverse=sorting_reverse)
			table = PrettyTable(map(lambda t: t[0], self.table_mapping))
			for entry in list_entries:
				entry_data = [mapping(entry) for _, mapping in self.table_mapping]
				table.add_row(entry_data)
			print(table)

			print('__________ Akcije __________')
			for i, (naziv_akcije, _) in enumerate(self.akcije):
				print(f' {i + 1}) {naziv_akcije}')
			print(f' X) Vrati se nazad')
			print('____________________________')
			akcija = input('Akcija: ').strip().upper()
			if akcija == 'X':
				return
			elif akcija.isdigit():
				self.process_action(int(akcija) - 1)
			else:
				print(' * Nevalidna vrednost akcije')
				input()

	def process_action(self, akcija_num):
		if akcija_num < 0 or akcija_num >= len(self.akcije):
			print(' * Nevalidna vrednost akcije')
			input()
			return
		self.akcije[akcija_num][1]()

	def promena_sortiranja(self):
		clear_screen()
		if self.__current_sorting is None:
			trenutni_metod_sortiranja = 'proizvoljno sistemu'
		elif self.__current_sorting == 'default':
			trenutni_metod_sortiranja = 'podrazumevano'
		else:
			trenutni_metod_sortiranja = self.__current_sorting
		lista_sortiranja = list(self.list_sortings.keys())
		print(f'''\
 === PROMENA SORTIRANJA ===
 Trenutno sortiranje: {trenutni_metod_sortiranja}

_______ Moguci metodi sortiranja _______
''')
		for i, naziv_sortiranja in enumerate(lista_sortiranja):
			if naziv_sortiranja == 'default':
				naziv_sortiranja = 'podrazumevano'
			print(f' {i + 1}) {naziv_sortiranja.title()}')
		print('________________________________________')
		while True:
			metod_sortiranja = input('Metod sortiranja: ').strip()
			if not metod_sortiranja.isdigit():
				print(' * Nevalidna vrednost metoda sortiranja')
			else:
				num_metod_sortiranja = int(metod_sortiranja) - 1
				if num_metod_sortiranja < 0 or num_metod_sortiranja >= len(lista_sortiranja):
					print(' * Nevalidna vrednost metoda sortiranja')
				else:
					self.__current_sorting = lista_sortiranja[num_metod_sortiranja]
					izabran_metod = 'podrazumevano' if self.__current_sorting == 'default' else self.__current_sorting
					print(f'Metod sortiranja liste je uspesno promenjen na "{izabran_metod}"')
					input()
					return

	def prikaz_pojedinacnog_unos(self):
		id_trazenog_str = input('ID Objekta: ').strip()
		if not id_trazenog_str.isdigit():
			print(' * ID mora biti broj')
			input()
		else:
			id_trazenog = int(id_trazenog_str)
			if id_trazenog not in self.list_entries_dict:
				print(' * Ne postoji objekat sa trazenim ID-om')
				input()
			else:
				entity = self.list_entries_dict[id_trazenog]
				self.prikaz_pojedinacnog.__func__(entity)
