from .korisnik_panel import KorisnikPanel
from businesslayer import KorisnikLogic
from .shared_functionality import ocene_ucenika_tabela

class UcenikPanel(KorisnikPanel):
	@property
	def panel_heading(self):
		return ' === UCENIK PANEL ==='

	@property
	def user_identity(self):
		ucenik = self.korisnik
		slusanja = KorisnikLogic.get_uceniks_slusa(ucenik)
		predmetna_tabela = ocene_ucenika_tabela(slusanja)
		return f'''\
 Ulogovani ste kao ucenik {ucenik.ime} {ucenik.prezime} ({ucenik.username})
 Razred: {ucenik.razred.godina}

 Podaci o predmetima koje slusate:
{predmetna_tabela}
'''