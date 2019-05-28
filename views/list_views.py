from businesslayer import PredmetLogic
from .prikaz_view import ListAllView

def dozvoljeni_razredi_str(predmet):
	razredi = ', '.join(map(lambda razred: str(razred.godina), predmet.razredi))
	if len(razredi) == 0:
		razredi = '/'
	return razredi				

class AdminPredmetList(ListAllView):
	list_heading = ' === Prikaz svih predmeta ==='
	table_mapping = [
		('ID', lambda predmet: predmet.id),
		('NAZIV', lambda predmet: predmet.naziv),
		('DOZVOLJENI RAZREDI', dozvoljeni_razredi_str),
	]
	list_sortings = {
		'default': (lambda predmet: predmet.naziv, False),
		'Opadajuce po ID-u': (lambda predmet: predmet.id, True)
	}

	def list_supplier(self):
		return PredmetLogic.get_all_predmet()
