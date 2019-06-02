from businesslayer import KorisnikLogic, InvalidKorisnikInfoError, PredmetLogic, UpdateInfoError
from utils import clear_screen, pretty_text_format
from prettytable import PrettyTable
from .shared_functionality import try_again
from .list_views import ProfesorPredmetList, ProfesorPredmetSlusasList

def prikaz_pojedinacnog_predmeta(profesor, predmet):
	class CustomProfesorPredmetSlusasList(ProfesorPredmetSlusasList):
		list_heading = f'Ucenici koji pohadjaju predmet {predmet.naziv} kod profesora {profesor.ime} {profesor.prezime}:'

		def list_supplier(self):
			slusas = KorisnikLogic.get_profesors_predmets_slusa(predmet, profesor)
			if slusas is None:
				return None
			return {slusa.ucenik.id: slusa for slusa in slusas}
	CustomProfesorPredmetSlusasList()

def prikaz_predmeta_profesora(profesor):
	class CustomProfesorPredmetList(ProfesorPredmetList):
		list_heading = f' === Prikaz predmeta profesora {profesor.ime} {profesor.prezime} ==='
		prikaz_pojedinacnog = lambda predmet: prikaz_pojedinacnog_predmeta(profesor, predmet)

		def list_supplier(self):
			return PredmetLogic.get_profesors_predmets(profesor)
	CustomProfesorPredmetList()