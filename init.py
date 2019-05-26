import argparse
from database import init_db, session_scope
from businesslayer import KorisnikLogic, InvalidKorisnikInfoError, RazredLogic
import getpass
from config import LOCAL_DATABASE_NAME
import os
from models import *
import config

def main():
	parser = argparse.ArgumentParser(description='Initialize database')
	parser.add_argument('--auto', dest='auto_init', action='store_true',
						help='Automatically initialize the system')
	parser.set_defaults(auto_init=False)
	args = parser.parse_args()

	try:
		if os.path.exists(LOCAL_DATABASE_NAME):
			if not args.auto_init:
				hard_reset = input('Baza vec postoji, zelite li da je obrisete i krenete iz pocetka [D/n] ')\
					.strip().upper() not in ['N', 'NE']
				if not hard_reset:
					raise Exception()
			os.remove(LOCAL_DATABASE_NAME)
		init_db()
		print('Struktura baze uspesno inicijalizovana')
		username, password = None, None
		if args.auto_init:
			username, password = 'admin', 'admin12345'
		else:
			print(' === UNOS ADMINISTRATOROVOG NALOGA === ')
			while True:
				try:
					username = input('Unesite korisnicko ime: ').strip()
					KorisnikLogic.validate_username(username)
					password = getpass.getpass('Unesite lozinku: ').strip()
					KorisnikLogic.validate_password(password)
					while True:
						password_confirmation = getpass.getpass('Potvrdite lozinku: ').strip()
						if password == password_confirmation:
							break
						else:
							print('Unete lozinke se ne poklapaju, pokusajte ponovo')
					break
				except InvalidKorisnikInfoError as e:
					print(' * Greska:', e)
					if not input('Zelite li da pokusate ponovo? [D/n] ').strip().upper()\
								 not in ['N', 'NE']:
						raise
		if KorisnikLogic.register_user(username=username, password=password, uloga='admin'):
			print('Administratorov nalog je uspesno dodat')
		else:
			print('Doslo je do greske prilikom dodavanja administratorovog naloga')
			raise Exception()

		razredi_ok = True
		for godina in range(config.MINIMUM_RAZRED, config.MAXIMUM_RAZRED + 1):
			razredi_ok &= RazredLogic.add_razred(godina)
		if not razredi_ok:
			print('Doslo je do greske prilikom dodavanja razreda')
			raise Exception()

		print('Razredi su uspesno dodati')

		print('Sistem je inicijalizovan i spreman za koriscenje')
	except:
		print('Doslo je do greske prilikom inicijalizacije sistema')



if __name__ == "__main__":
	main()