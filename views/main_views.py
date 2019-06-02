from businesslayer import KorisnikLogic, InvalidKorisnikInfoError
from .shared_functionality import try_again
from utils import clear_screen
import getpass

def login():
	while True:
		print(' === PRIJAVLJIVANJE === ')

		username = input('Korisnicke ime: ')
		lozinka = getpass.getpass('Lozinka: ')
		korisnik = KorisnikLogic.authenticate_user(username, lozinka)
		if korisnik is None:
			print(' * Niste uneli postojece ime i lozinku')
			if not try_again():
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
	if korisnik is not None:
		korisnicki_panel(korisnik)
	print('Dovidjenja.')


def korisnicki_panel(korisnik):
	from models import Admin, Ucenik, Profesor

	if isinstance(korisnik, Admin):
		from .admin_views import AdminPanel
		AdminPanel(korisnik.id)
	elif isinstance(korisnik, Ucenik):
		from .ucenik_views import UcenikPanel
		UcenikPanel(korisnik.id)
	elif isinstance(korisnik, Profesor):
		from .profesor_views import ProfesorPanel
		ProfesorPanel(korisnik.id)