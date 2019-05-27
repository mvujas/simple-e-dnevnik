from businesslayer import KorisnikLogic, InvalidKorisnikInfoError, PredmetLogic
from utils import clear_screen
from prettytable import PrettyTable
from .korisnik_panel import KorisnikPanel
from .shared_functionality import try_again

class AdminPanel(KorisnikPanel):
	ACTION_DICTIONARY = KorisnikPanel.ACTION_DICTIONARY + [
		('Dodaj ucenika', lambda korisnik: dodavanje_regularnog_korisnika('ucenik')),
		('Dodaj profesora', lambda korisnik: dodavanje_regularnog_korisnika('profesor')),
		('Dodaj predmet', lambda korisnik: dodavanje_predmeta()),
		('Prikazi predmete', lambda korisnik: prikaz_predmeta()),
		
	]

	@property
	def panel_heading(self):
		return ' === ADMIN PANEL ==='

	@property
	def user_identity(self):
		return 'Ulogovani ste kao administrator {}'.format(self.korisnik.username) 


def dodavanje_regularnog_korisnika(uloga):
	uloga = uloga.strip()
	while True:
		clear_screen()
		print(' === Dodavanje {}a ==='.format(uloga))

		username = input('Korisnicko ime: ')
		password = input('Sifra: ')
		ime = input('Ime: ')
		prezime = input('Prezime: ')

		args = {
			'username': username,
			'password': password,
			'ime': ime,
			'prezime': prezime,
			'uloga': uloga
		}

		if uloga == 'ucenik':
			razred = None
			while True:
				razred = input('Razred: ').strip()
				if razred.isdigit():
					break
				else:
					print(' * Razred mora biti ceo broj!')
			razred = int(razred)
			args['razred'] = razred

		try:
			KorisnikLogic.register_user(**args)
			print('{} je uspesno dodat'.format(uloga.title()))
			return
		except InvalidKorisnikInfoError as e:
			print(' * Greska:', e)
			if not try_again():
				return


def dodavanje_predmeta():
	while True:
		clear_screen()
		print(' === Dodavanje predmeta ===')
		print(' *** Napomena: Svi predmeti moraju imati razlicito ime ***')
		naziv = input('Naziv: ')
		success = PredmetLogic.add_predmet(naziv)
		if success:
			print('Predmet je uspesno dodat')
			return
		else:
			print('''\
 * Doslo je do greske prilikom dodavanja predmeta,
   proverite da li vec postoji predmet sa datim imenom\
''')
			if not try_again():
				return


def prikaz_predmeta():
	while True:
		clear_screen()
		predmeti = PredmetLogic.get_all_predmet()
		print(' === Prikaz predmeta ===')
		if predmeti is None:
			print('Doslo je do greske prilikom ucitavanja predmeta')
		else:
			table = PrettyTable(['ID', 'NAZIV', 'DOZVOLJENI RAZREDI'])
			for predmet in predmeti.values():
				razredi = ', '.join(map(lambda razred: str(razred.godina), predmet.razredi))
				if len(razredi) == 0:
					razredi = '/'
				table.add_row([str(predmet.id), predmet.naziv, razredi])
			print(table)
		while True:
			print()
			odabir_izmene = input('Zelite li da izmenite neki predmet[Ako zelite unesite njegov ID, u suprotnom ostavite prazno]: ').strip()
			if odabir_izmene == '':
				return
			elif not odabir_izmene.isdigit():
				print(' * Nevalidan unos')
				if not try_again():
					return
			else:
				id = int(odabir_izmene)
				if id not in predmeti:
					print(' * Ne postoji predmet pod unetim id-om')
					if not try_again():
						return
				else:
					izmena_predmeta(id)
					break


def izmena_predmeta(predmet_id):
	predmet = PredmetLogic.get_predmet_by_pk(predmet_id) 
	clear_screen()
	razredi = ', '.join(map(lambda razred: str(razred.godina), predmet.razredi))
	if len(razredi) == 0:
		razredi = 'nije dozvoljeno ni u jednom razredu'
	print(f'''\
 === Izmena predmeta ===
  Predmet {predmet.naziv} [id {predmet.id}]
  Dozvoljeni razredi: {razredi}

  Akcije:
  1) Promena imena
  2) Dodavanje dozvoljenih razreda
  X) Povratak\
''')
	while True:
		akcija = input('Izaberite akciju: ').strip()
		if akcija in ['x', 'X']:
			return
		elif akcija == '1':
			promena_imena_predmeta(predmet)
			izmena_predmeta(predmet_id)
			return
		elif akcija == '2':
			pass
		else:
			print(' * Nevalidna vrednost akcije')


def promena_imena_predmeta(predmet):
	naziv = input('Novi naziv predmeta: ').strip()
	if PredmetLogic.update_predmet_name(predmet, naziv):
		print('Naziv predmeta uspesno promenjen')
	else:
		print(' * Doslo je do greske prilikom promene naziva predmeta')
	input()