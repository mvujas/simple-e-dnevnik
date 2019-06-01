from businesslayer import PredmetLogic, KorisnikLogic
from .prikaz_view import ListAllView
from .shared_functionality import dozvoljeni_razredi_str		
from .entity_views import AdminPredmetView, AdminProfesorView

def predmeti_profesora_str(profesor):
	predmeti = ', '.join(map(lambda predmet: predmet.naziv, profesor.predmeti))
	if len(predmeti) == 0:
		predmeti = '/'
	return predmeti

class AdminPredmetList(ListAllView):
	list_heading = ' === Prikaz svih predmeta ==='
	table_mapping = [
		('ID', lambda predmet: predmet.id),
		('NAZIV', lambda predmet: predmet.naziv),
		('DOZVOLJENI RAZREDI', dozvoljeni_razredi_str),
	]
	list_sortings = {
		'default': (lambda predmet: predmet.id, False),
		'Opadajuce po ID-u': (lambda predmet: predmet.id, True),
		'Rastuce po nazivu': (lambda predmet: predmet.naziv, False),
	}
	prikaz_pojedinacnog = lambda predmet: AdminPredmetView(
		lambda: PredmetLogic.get_predmet_by_pk(predmet.id))

	def list_supplier(self):
		return PredmetLogic.get_all_predmet()

class AdminUcenikList(ListAllView):
	list_heading = ' === Prikaz svih ucenika ==='
	table_mapping = [
		('ID', lambda ucenik: ucenik.id),
		('IME I PREZIME', lambda ucenik: f'{ucenik.ime} {ucenik.prezime}'),
		('GODINA', lambda ucenik: ucenik.razred.godina),
	]
	list_sortings = {
		'default': (lambda ucenik: ucenik.id, False),
	}

	def list_supplier(self):
		return KorisnikLogic.get_all_ucenik()

class AdminProfesorList(ListAllView):
	list_heading = ' === Prikaz svih profesora ==='
	table_mapping = [
		('ID', lambda profesor: profesor.id),
		('IME I PREZIME', lambda profesor: f'{profesor.ime} {profesor.prezime}'),
		('PREDMETI', predmeti_profesora_str)
	]
	list_sortings = {
		'default': (lambda profesor: profesor.id, False),
	}
	prikaz_pojedinacnog = lambda profesor: AdminProfesorView(
		lambda: KorisnikLogic.get_profesor_by_pk(profesor.id))

	def list_supplier(self):
		return KorisnikLogic.get_all_profesor()
