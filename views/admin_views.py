from .korisnik_panel import KorisnikPanel
from .admin_panel_additional_functionality import dodavanje_regularnog_korisnika, dodavanje_predmeta, prikaz_ucenika
from .list_views import AdminPredmetList

class AdminPanel(KorisnikPanel):
	ACTION_DICTIONARY = KorisnikPanel.ACTION_DICTIONARY + [
		('Dodaj ucenika', lambda korisnik: dodavanje_regularnog_korisnika('ucenik')),
		('Dodaj profesora', lambda korisnik: dodavanje_regularnog_korisnika('profesor')),
		('Dodaj predmet', lambda korisnik: dodavanje_predmeta()),
		('Prikazi ucenike', lambda korisnik: prikaz_ucenika()),
		('Prikazi predmete', lambda korisnik: AdminPredmetList()),
	]

	@property
	def panel_heading(self):
		return ' === ADMIN PANEL ==='

	@property
	def user_identity(self):
		return 'Ulogovani ste kao administrator {}'.format(self.korisnik.username) 