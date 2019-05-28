from businesslayer import KorisnikLogic, InvalidKorisnikInfoError, PredmetLogic
from utils import clear_screen
from prettytable import PrettyTable
from .shared_functionality import try_again


def dodavanje_regularnog_korisnika(uloga):
	uloga = uloga.strip()
	while True:
		clear_screen()
		print(' === Dodavanje {}a ==='.format(uloga))

		username = input('Korisnicko ime: ')
		password = input('Sifra: ')
		ime = input('Ime: ')
		prezime = input('Prezime: ')

		args = {
			'username': username,
			'password': password,
			'ime': ime,
			'prezime': prezime,
			'uloga': uloga
		}

		if uloga == 'ucenik':
			razred = None
			while True:
				razred = input('Razred: ').strip()
				if razred.isdigit():
					break
				else:
					print(' * Razred mora biti ceo broj!')
			razred = int(razred)
			args['razred'] = razred

		try:
			KorisnikLogic.register_user(**args)
			print('{} je uspesno dodat'.format(uloga.title()))
			return
		except InvalidKorisnikInfoError as e:
			print(' * Greska:', e)
			if not try_again():
				return


def dodavanje_predmeta():
	while True:
		clear_screen()
		print(' === Dodavanje predmeta ===')
		print(' *** Napomena: Svi predmeti moraju imati razlicito ime ***')
		naziv = input('Naziv: ')
		success = PredmetLogic.add_predmet(naziv)
		if success:
			print('Predmet je uspesno dodat')
			return
		else:
			print('''\
 * Doslo je do greske prilikom dodavanja predmeta,
   proverite da li vec postoji predmet sa datim imenom\
''')
			if not try_again():
				return


def prikaz_predmeta():
	while True:
		clear_screen()
		predmeti = PredmetLogic.get_all_predmet()
		print(' === Prikaz predmeta ===')
		if predmeti is None:
			print('Doslo je do greske prilikom ucitavanja predmeta')
		else:
			table = PrettyTable(['ID', 'NAZIV', 'DOZVOLJENI RAZREDI'])
			for predmet in predmeti.values():
				razredi = ', '.join(map(lambda razred: str(razred.godina), predmet.razredi))
				if len(razredi) == 0:
					razredi = '/'
				table.add_row([str(predmet.id), predmet.naziv, razredi])
			print(table)
		while True:
			print()
			odabir_izmene = input('Zelite li da izmenite neki predmet[Ako zelite unesite njegov ID, u suprotnom ostavite prazno]: ').strip()
			if odabir_izmene == '':
				return
			elif not odabir_izmene.isdigit():
				print(' * Nevalidan unos')
				if not try_again():
					return
			else:
				id = int(odabir_izmene)
				if id not in predmeti:
					print(' * Ne postoji predmet pod unetim id-om')
					if not try_again():
						return
				else:
					izmena_predmeta(id)
					break


def izmena_predmeta(predmet_id):
	predmet = PredmetLogic.get_predmet_by_pk(predmet_id) 
	clear_screen()
	razredi = ', '.join(map(lambda razred: str(razred.godina), predmet.razredi))
	if len(razredi) == 0:
		razredi = 'nije dozvoljeno ni u jednom razredu'
	print(f'''\
 === Izmena predmeta ===
  Predmet {predmet.naziv} [id {predmet.id}]
  Dozvoljeni razredi: {razredi}

  Akcije:
  1) Promena imena
  2) Promeni dozvoljene razrede
  X) Povratak\
''')
	while True:
		akcija = input('Izaberite akciju: ').strip()
		if akcija in ['x', 'X']:
			return
		elif akcija == '1':
			promena_imena_predmeta(predmet)
			izmena_predmeta(predmet_id)
			return
		elif akcija == '2':
			promena_dozvoljenih_razreda(predmet)
			izmena_predmeta(predmet_id)
			return
		else:
			print(' * Nevalidna vrednost akcije')


def promena_imena_predmeta(predmet):
	clear_screen()
	print(f'''\
 === Promena naziva predmeta ===
 Predmet {predmet.naziv} [id {predmet.id}]
''')
	naziv = input('Novi naziv predmeta: ').strip()
	if PredmetLogic.update_predmet_name(predmet, naziv):
		print('Naziv predmeta uspesno promenjen')
	else:
		print(' * Doslo je do greske prilikom promene naziva predmeta')
	input()

def promena_dozvoljenih_razreda(predmet):
	clear_screen()
	print(f'''\
 === Proma dozvoljenih razreda predmeta ===
 Predmet {predmet.naziv} [id {predmet.id}]
''')
	while True:
		unos = input('Unesite razrede u kojima zelite da se predmet slusa odvojene zarezom: ').strip()
		try:
			razredi = map(lambda razred: int(razred.strip()), unos.split(','))
			break
		except:
			print('Nevalidan format ulaza')
			if not try_again:
				return
	if PredmetLogic.set_razreds_to_predmet(predmet, *razredi):
		print('Dozvoljeni razredi predmeta su uspesno promenjeni')
	else:
		print(' * Doslo je do greske prilikom promene dozvoljenih razreda')
	input()

def prikaz_ucenika():
	while True:
		clear_screen()
		ucenici = KorisnikLogic.get_all_ucenik()
		print(' === Prikaz ucenika ===')
		if ucenici is None:
			print('Doslo je do greske prilikom ucitavanja ucenika')
		else:
			table = PrettyTable(['ID', 'IME', 'PREZIME', 'RAZRED'])
			for ucenik in ucenici.values():
				table.add_row([str(ucenik.id), ucenik.ime, ucenik.prezime, str(ucenik.razred.godina)])
			print(table)
		while True:
			print()
			odabir_izmene = input('Zelite li da izmenite nekog ucenika[Ako zelite unesite njegov ID, u suprotnom ostavite prazno]: ').strip()
			if odabir_izmene == '':
				return
			elif not odabir_izmene.isdigit():
				print(' * Nevalidan unos')
				if not try_again():
					return
			else:
				id = int(odabir_izmene)
				if id not in ucenici:
					print(' * Ne postoji ucenik pod unetim id-om')
					if not try_again():
						return
				else:
					izmena_ucenika(id)
					break

def izmena_ucenika(ucenik_id):
	ucenik = KorisnikLogic.get_korisnik_by_pk(ucenik_id)
	print(ucenik)
	input()
	return 
	clear_screen()
	print(f'''\
 === Izmena ucenika ===
  Ucenik {ucenik.ime} {ucenik.prezime} [username {ucenik.username}]
  	Razred {ucenik.razred.godina}

  Akcije:
  1) Promena imena
  2) Promeni dozvoljene razrede
  X) Povratak\
''')
	while True:
		akcija = input('Izaberite akciju: ').strip()
		if akcija in ['x', 'X']:
			return
		elif akcija == '1':
			#promena_imena_predmeta(predmet)
			#izmena_predmeta(predmet_id)
			return
		elif akcija == '2':
			#promena_dozvoljenih_razreda(predmet)
			#izmena_predmeta(predmet_id)
			return
		else:
			print(' * Nevalidna vrednost akcije')
	print('Not implemented yet...')
	input()
