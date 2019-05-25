from .korisnik_panel import KorisnikPanel

class ProfesorPanel(KorisnikPanel):
	@property
	def panel_heading(self):
		return ' === PROFESOR PANEL ==='

	@property
	def user_identity(self):
		return 'Ulogovani ste kao profesor {} {} ({})'.format(\
			self.korisnik.ime, self.korisnik.prezime, self.korisnik.username) 