from .korisnik_panel import KorisnikPanel
from .profesor_panel_additional_functionality import *

class ProfesorPanel(KorisnikPanel):
	ACTION_DICTIONARY = KorisnikPanel.ACTION_DICTIONARY + [
		('Pregled predmeta', prikaz_predmeta_profesora)
	]

	@property
	def panel_heading(self):
		return ' === PROFESOR PANEL ==='

	@property
	def user_identity(self):
		return 'Ulogovani ste kao profesor {} {} ({})'.format(\
			self.korisnik.ime, self.korisnik.prezime, self.korisnik.username) 