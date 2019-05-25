from .korisnik_panel import KorisnikPanel

class UcenikPanel(KorisnikPanel):
	@property
	def panel_heading(self):
		return ' === UCENIK PANEL ==='

	@property
	def user_identity(self):
		return 'Ulogovani ste kao ucenik {} {} ({})'.format(\
			self.korisnik.ime, self.korisnik.prezime, self.korisnik.username)