from businesslayer import KorisnikLogic, InvalidKorisnikInfoError
from utils import clear_screen
import getpass

def try_again():
	return input('Zelite li da pokusate ponovo? [D/n] ').strip().upper() not in ['N', 'NE']


def change_username(korisnik):
	while True:
		clear_screen()
		print(' === PROMENA KORISNICKOG IMENA === ')
		try:
			new_username = input('Unesite novo korisnicko ime: ')
			success = KorisnikLogic.change_username(korisnik, new_username)
			if success:
				print('Uspesno ste promenili korisnicko ime')
			else:
				print('Doslo je do greske prilikom promene korisnickog imena, pokusajte kasnije')
			input()
			return
		except InvalidKorisnikInfoError as e:
			print(' * Greska:', e)
			if not try_again():
				return


def change_password(korisnik):
	while True:
		clear_screen()
		print(' === PROMENA LOZINKE === ')
		try:
			new_password = getpass.getpass('Unesite novu lozinku: ').strip()
			KorisnikLogic.validate_password(new_password)
			while True:
				password_confirmation = getpass.getpass('Potvrdite lozinku: ').strip()
				if new_password == password_confirmation:
					break
				else:
					print('Unete lozinke se ne poklapaju, pokusajte ponovo')
			success = KorisnikLogic.change_password(korisnik, new_password)
			if success:
				print('Uspesno ste promenili lozinku')
			else:
				print('Doslo je do greske prilikom promene lozinke, pokusajte kasnije')
			input()
			return
		except InvalidKorisnikInfoError as e:
			print(' * Greska:', e)
			if not try_again():
				return

def dozvoljeni_razredi_str(predmet):
	razredi = ', '.join(map(lambda razred: str(razred.godina), predmet.razredi))
	if len(razredi) == 0:
		razredi = '/'
	return razredi		

def predmeti_profesora_str(profesor):
	predmeti = ', '.join(map(lambda predmet: predmet.naziv, profesor.predmeti))
	if len(predmeti) == 0:
		predmeti = '/'
	return predmeti