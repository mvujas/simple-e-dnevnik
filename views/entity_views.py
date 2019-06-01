from .single_entity_view import EntityView
from .shared_functionality import dozvoljeni_razredi_str
from .admin_panel_additional_functionality import promena_imena_predmeta, \
		promena_imena_regularnog_korisnika, promena_prezimena_regularnog_korisnika

def informacije_o_predmetu(predmet):
	dozvoljeni_razredi = dozvoljeni_razredi_str(predmet)
	return f'''\
 Predmet {predmet.naziv}
 Slusa se u razredima: {dozvoljeni_razredi}
'''

class AdminPredmetView(EntityView):
	heading = ' === Prikaz predmeta ==='
	entity_info_function = informacije_o_predmetu
	ACTION_DICTIONARY = [
		('Promeni naziv', promena_imena_predmeta)
	]

def informacije_o_profesoru(profesor):
	return f'''\
 Profesor {profesor.ime} {profesor.prezime}
'''

class AdminProfesorView(EntityView):
	heading = ' === Prikaz profesora ==='
	entity_info_function = informacije_o_profesoru
	ACTION_DICTIONARY = [
		('Promeni ime', promena_imena_regularnog_korisnika),
		('Promeni prezime', promena_prezimena_regularnog_korisnika)
	]