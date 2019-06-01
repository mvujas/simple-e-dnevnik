from businesslayer import KorisnikLogic, InvalidKorisnikInfoError, PredmetLogic, UpdateInfoError
from utils import clear_screen
from prettytable import PrettyTable
from .shared_functionality import try_again

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

def promena_imena_predmeta(predmet):
	naziv = input('Novi naziv: ').strip()
	try:
		if PredmetLogic.change_predmet_naziv(predmet, naziv):
			print('Naziv predmeta uspesno promenjen')
		else:
			print(' * Doslo je do greske prilikom promene naziva predmeta')
	except UpdateInfoError as e:
		print(' * Greska:', e)
	input()

def promena_imena_regularnog_korisnika(korisnik):
	ime = input('Novo ime: ').strip()
	try:
		if KorisnikLogic.change_ime(korisnik, ime):
			print('Ime korisnika je uspesno promenjen')
		else:
			print(' * Doslo je do greske prilikom promene imena korisnika')
	except InvalidKorisnikInfoError as e:
		print(' * Greska:', e)
	input()

def promena_prezimena_regularnog_korisnika(korisnik):
	prezime = input('Novo prezime: ').strip()
	try:
		if KorisnikLogic.change_prezime(korisnik, prezime):
			print('Prezime korisnika je uspesno promenjen')
		else:
			print(' * Doslo je do greske prilikom promene prezimena korisnika')
	except InvalidKorisnikInfoError as e:
		print(' * Greska:', e)
	input()

