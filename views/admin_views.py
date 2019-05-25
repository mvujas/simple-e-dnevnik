from .korisnik_panel import KorisnikPanel
from businesslayer import KorisnikLogic, InvalidKorisnikInfoError
from utils import clear_screen

class AdminPanel(KorisnikPanel):
	ACTION_DICTIONARY = KorisnikPanel.ACTION_DICTIONARY + [
		('Dodaj ucenika', lambda korisnik: dodavanje_regularnog_korisnika('ucenik')),
		('Dodaj profesora', lambda korisnik: dodavanje_regularnog_korisnika('profesor')),
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

		try:
			KorisnikLogic.register_user(
				username=username, 
				password=password,
				ime=ime,
				prezime=prezime, 
				uloga=uloga)
			print('{} je uspesno dodat'.format(uloga.title()))
			return
		except InvalidKorisnikInfoError as e:
			print(' * Greska:', e)
			pokusati_ponovo = input('Zelite li da pokusate ponovo? [D/n] ').strip().upper() \
								not in ['N', 'NE']
			if not pokusati_ponovo:
				return