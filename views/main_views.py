from businesslayer import KorisnikLogic, InvalidKorisnikInfoError
import getpass
from utils import clear_screen

def login():
	while True:
		print(' === PRIJAVLJIVANJE === ')

		username = input('Korisnicke ime: ')
		lozinka = getpass.getpass('Lozinka: ')
		korisnik = KorisnikLogic.authenticate_user(username, lozinka)
		if korisnik is None:
			print(' * Niste uneli postojece ime i lozinku')
			pokusati_ponovo = input('Zelite li da pokusate ponovo? [D/n] ').strip().upper() \
								not in ['N', 'NE']
			if not pokusati_ponovo:
				return None
			clear_screen()
		else:
			return korisnik

def main_view():
	clear_screen()
	print(
'''\
---------------------------
 Dobrodosli u E-Dnevnik

 Da biste nastavili dalje
 morate se prijaviti
---------------------------
''')
	korisnik = login()
	if korisnik is None:
		return
	korisnicki_panel(korisnik)
	print('Dovidjenja.')


def korisnicki_panel(korisnik):
	from models import Admin, Ucenik, Profesor

	if isinstance(korisnik, Admin):
		from .admin_views import AdminPanel
		AdminPanel(korisnik)
	elif isinstance(korisnik, Ucenik):
		from .ucenik_views import UcenikPanel
		UcenikPanel(korisnik)
	elif isinstance(korisnik, Profesor):
		from .profesor_views import ProfesorPanel
		ProfesorPanel(korisnik)