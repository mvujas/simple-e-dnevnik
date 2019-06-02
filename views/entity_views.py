from .single_entity_view import EntityView
from businesslayer import KorisnikLogic, UpdateInfoError, PredmetLogic
from .shared_functionality import dozvoljeni_razredi_str, predmeti_profesora_str, predmeti_ucenika_str, \
		ocene_odvojene_zarezom, srednja_vrednost_ocena
from .admin_panel_additional_functionality import promena_imena_predmeta, \
		promena_imena_regularnog_korisnika, promena_prezimena_regularnog_korisnika, \
		dodavanje_razreda_predmetu, dodavanje_predmeta_profesoru, dodavanje_slusa_uceniku

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
		('Promeni naziv', promena_imena_predmeta),
		('Dodaj razred u kojem se slusa', dodavanje_razreda_predmetu)
	]

def informacije_o_profesoru(profesor):
	predmeti = predmeti_profesora_str(profesor)
	return f'''\
 Profesor {profesor.ime} {profesor.prezime}
 predaje: {predmeti}
'''

class AdminProfesorView(EntityView):
	heading = ' === Prikaz profesora ==='
	entity_info_function = informacije_o_profesoru
	ACTION_DICTIONARY = [
		('Promeni ime', promena_imena_regularnog_korisnika),
		('Promeni prezime', promena_prezimena_regularnog_korisnika),
		('Dodaj predmet', dodavanje_predmeta_profesoru)
	]

def informacije_o_uceniku(ucenik):
	slusas = KorisnikLogic.get_uceniks_slusa(ucenik)

	return f'''\
 Ucenik {ucenik.ime} {ucenik.prezime}
 pohadja {ucenik.razred.godina}. razred

 Predmeti koje slusa: {'Greska u toku ucitavanja' if slusas is None else predmeti_ucenika_str(slusas)}
'''

class AdminUcenikView(EntityView):
	heading = ' === Prikaz ucenika ==='
	entity_info_function = informacije_o_uceniku
	ACTION_DICTIONARY = [
		('Promeni ime', promena_imena_regularnog_korisnika),
		('Promeni prezime', promena_prezimena_regularnog_korisnika),
		('Dodaj predmet da slusa', dodavanje_slusa_uceniku)
	]

def informacije_o_slusa(slusa):
	ocene = ocene_odvojene_zarezom(slusa.ocene)
	srednja_ocena = srednja_vrednost_ocena(slusa.ocene)
	return f'''\
 Ucenik {slusa.ucenik.ime} {slusa.ucenik.prezime} (razred {slusa.ucenik.razred.godina}.)
 Predmet {slusa.predmet.naziv}

 Ocene {ocene} (srednja vrednost {srednja_ocena})
'''

def dodavanje_ocene(slusa):
	ocena_str = input('Vrednost ocene: ').strip()
	if not ocena_str.isdigit():
		print(' * Vrednost ocene mora biti ceo broj izmedju 1 i 5')
	else:
		ocena = int(ocena_str)
		if ocena < 1 or ocena > 5:
			print(' * Vrednost ocene mora biti ceo broj izmedju 1 i 5')
		else:
			try:
				if PredmetLogic.add_ocena_with_slusa(slusa, ocena):
					print('Ocena je uspesno dodata')
				else:
					print(' * Doslo je do greske prilikom dodavanja ocene')
			except UpdateInfoError as e:
				print(' * Greska:', e)
	input()

class ProfesorPanelSlusaView(EntityView):
	heading = ' === Prikaz podataka ucenika za predmet ==='
	entity_info_function = informacije_o_slusa
	ACTION_DICTIONARY = [
		('Dodaj ocenu', dodavanje_ocene),
	]