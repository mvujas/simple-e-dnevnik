from dataaccesslayer import DAOManager
from utils import debug_print
from models import *
from database import session_scope
from .exceptions import UpdateInfoError, InvalidKorisnikInfoError
from .razred_logic import RazredLogic
import traceback
import bcrypt
import config
import re

class KorisnikLogic:
	@staticmethod
	def validate_name(subject, name):
		if len(name) < config.MINIMUM_NAME_LENGTH:
			raise InvalidKorisnikInfoError('%s mora biti duzine barem %d' % (subject.title(), config.MINIMUM_NAME_LENGTH))
		if not name.replace(' ', '').isalpha():
			raise InvalidKorisnikInfoError('%s moze sadrzati samo slova i razmake' % subject.title())
		
	@staticmethod
	def validate_username(username):
		if len(username) < config.MINIMUM_USERNAME_LENGTH:
			raise InvalidKorisnikInfoError('Username mora biti duzine barem %d' % config.MINIMUM_USERNAME_LENGTH)
		if not username.isalnum():
			raise InvalidKorisnikInfoError('Username moze sadrzati samo slova i brojeve')

	@staticmethod
	def validate_password(password):
		if len(password) < config.MINIMUM_PASSWORD_LENGTH:
			raise InvalidKorisnikInfoError('Sifra mora biti duzine barem %d' % config.MINIMUM_PASSWORD_LENGTH)
		if not re.match('^[-_.@\\d\\w]*$', password):
			raise InvalidKorisnikInfoError('Sifra moze sadrzati samo slova, brojeve i znakove -, _, ., @')

	@staticmethod
	def register_user(**params):
		korisnik = None
		try:
			uloga = params['uloga'].strip().lower()
			username = params['username'].strip()
			KorisnikLogic.validate_username(username)
			password = params['password'].strip()
			KorisnikLogic.validate_password(password)
			password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
			if uloga in ['admin', 'administrator']:
				korisnik = Admin(username, password)
			else:
				assert uloga in ['ucenik', 'profesor']
				ime = params['ime'].strip()
				prezime = params['prezime'].strip()
				KorisnikLogic.validate_name('ime', ime)
				KorisnikLogic.validate_name('prezime', prezime)
				if uloga == 'profesor':
					korisnik = Profesor(username, password, ime, prezime)
				else:
					godina = params['razred']
					if not isinstance(godina, int):
						raise InvalidKorisnikInfoError('Razred mora biti ceo broj')
					razred = RazredLogic.get_razred_by_godina(godina)
					if razred is None:
						raise InvalidKorisnikInfoError('Uneti razred ne postoji')
					korisnik = Ucenik(username, password, ime, prezime, razred)
		except InvalidKorisnikInfoError:
			raise
		except:
			debug_print('Insufficient params passed to register_user\n', traceback.format_exc())
			return False

		dao = None
		try:
			with session_scope() as session:
				dao = DAOManager.get_korisnik_dao(session)
				if dao.get_korisnik_by_username(korisnik.username) is not None:
					raise InvalidKorisnikInfoError('Vec postoji korisnik sa datim username-om')
				dao.add_korisnik(korisnik)
			return True
		except InvalidKorisnikInfoError:
			raise
		except:
			return False
		finally:
			DAOManager.release(dao)

	@staticmethod
	def do_passwords_match(korisnik, password):
		return bcrypt.checkpw(password.encode(), korisnik.password)

	@staticmethod
	def authenticate_user(username, password):
		dao = None
		try:
			username = username.strip()
			password = password.strip()
			with session_scope() as session:
				dao = DAOManager.get_korisnik_dao(session)
				user = dao.get_korisnik_by_username(username)
				if user is None:
					return None
				if KorisnikLogic.do_passwords_match(user, password):
					session.refresh(user)
					return user
				else:
					return None
		except:
			return None
		finally:
			DAOManager.release(dao)
	
	@staticmethod
	def change_ime(korisnik, ime):
		ime = ime.strip()
		dao = None
		try:
			KorisnikLogic.validate_name('ime', ime)
			with session_scope() as session:
				dao = DAOManager.get_korisnik_dao(session)
				dao.update_korisnik_attribute(korisnik, 'ime', ime)
			return True
		except InvalidKorisnikInfoError:
			raise
		except:
			return False
		finally:
			DAOManager.release(dao)

	@staticmethod
	def change_prezime(korisnik, prezime):
		prezime = prezime.strip()
		dao = None
		try:
			KorisnikLogic.validate_name('prezime', prezime)
			with session_scope() as session:
				dao = DAOManager.get_korisnik_dao(session)
				dao.update_korisnik_attribute(korisnik, 'prezime', prezime)
			return True
		except InvalidKorisnikInfoError:
			raise
		except:
			return False
		finally:
			DAOManager.release(dao)

	@staticmethod
	def change_username(korisnik, new_username):
		new_username = new_username.strip()
		dao = None
		try:
			KorisnikLogic.validate_username(new_username)
			with session_scope() as session:
				dao = DAOManager.get_korisnik_dao(session)
				if dao.get_korisnik_by_username(new_username) is not None:
					raise InvalidKorisnikInfoError('Vec postoji korisnik sa datim username-om')
				dao.update_korisnik_attribute(korisnik, 'username', new_username)
			return True
		except InvalidKorisnikInfoError:
			raise
		except:
			return False
		finally:
			DAOManager.release(dao)

	@staticmethod
	def change_password(korisnik, new_password):
		new_password = new_password.strip()
		dao = None
		try:
			KorisnikLogic.validate_password(new_password)
			with session_scope() as session:
				dao = DAOManager.get_korisnik_dao(session)
				dao.update_korisnik_attribute(korisnik, 'password', new_password)
			return True
		except:
			return False
		finally:
			DAOManager.release(dao)

	@staticmethod
	def get_korisnik_by_username(username):
		dao = None
		try:
			with session_scope() as session:
				dao = DAOManager.get_korisnik_dao(session)
				korisnik = dao.get_korisnik_by_username(username)
				if korisnik is not None:
					session.refresh(korisnik)
					return korisnik
				else:
					return None
		except:
			return None
		finally:
			DAOManager.release(dao)

	@staticmethod
	def get_korisnik_by_pk(primary_key): 
	# Ispostavilo se da fali session.refresh da bi radilo sa ostalim podklasama od korisnika (sto sam shvatio tek pri kraju pisanja programa)
	# ali posto se njihove pojedinacne metode vec koriste u velikom delu programa ostavicu tako da ne bih napravio slucajno neki bug
		dao = None
		try:
			with session_scope() as session:
				dao = DAOManager.get_korisnik_dao(session)
				korisnik = dao.get_korisnik_by_pk(primary_key)
				if korisnik is not None:
					session.refresh(korisnik)
					return korisnik
				else:
					return None
		except:
			return None
		finally:
			DAOManager.release(dao)		

	@staticmethod
	def __get_all_korisnik(korisnik_dao_call):
		dao = None
		try:
			with session_scope() as session:
				dao = DAOManager.get_korisnik_dao(session)
				korisnici = korisnik_dao_call(dao)
				if korisnici is None:
					return None
				else:
					return { korisnik.id: korisnik for korisnik in korisnici }
		except:
			return None
		finally:
			DAOManager.release(dao)

	@staticmethod
	def get_all_ucenik():
		return KorisnikLogic.__get_all_korisnik(lambda dao: dao.get_all_ucenik())

	@staticmethod
	def get_all_profesor():
		return KorisnikLogic.__get_all_korisnik(lambda dao: dao.get_all_profesor())

	@staticmethod
	def __get_korisnik_by_pk(korisnik_dao_call, primary_key):
		dao = None
		try:
			with session_scope() as session:
				dao = DAOManager.get_korisnik_dao(session)
				return korisnik_dao_call(dao, primary_key)
		except:
			return None
		finally:
			DAOManager.release(dao)

	@staticmethod
	def get_profesor_by_pk(primary_key):
		return KorisnikLogic.__get_korisnik_by_pk(
			lambda dao, id: dao.get_profesor_by_pk(id), primary_key)

	@staticmethod
	def get_ucenik_by_pk(primary_key):
		return KorisnikLogic.__get_korisnik_by_pk(
			lambda dao, id: dao.get_ucenik_by_pk(id), primary_key)

	@staticmethod
	def add_profesor_predmet_relation(profesor, predmet):
		dao = None
		try:
			with session_scope() as session:
				dao = DAOManager.get_korisnik_dao(session)
				if predmet in profesor.predmeti:
					raise UpdateInfoError('Profesor vec predaje uneti predmet')
				dao.add_predmet_to_profesor(profesor, predmet)
			return True
		except UpdateInfoError:
			raise
		except:
			return False
		finally:
			DAOManager.release(dao)

	@staticmethod
	def add_slusa(ucenik, predmet, profesor):
		dao = None
		try:
			with session_scope() as session:
				dao = DAOManager.get_korisnik_dao(session)
				if profesor not in predmet.profesori:
					raise UpdateInfoError('Profesor ne predaje uneti predmet')
				if dao.does_slusa_exists(ucenik, predmet):
					raise UpdateInfoError('Ucenik vec slusa dati predmet')
				dao.add_predmet_to_ucenik(ucenik, predmet, profesor)
			return True
		except UpdateInfoError:
			raise
		except:
			return False
		finally:
			DAOManager.release(dao)

	@staticmethod
	def get_uceniks_slusa(ucenik):
		dao = None
		try:
			with session_scope() as session:
				dao = DAOManager.get_korisnik_dao(session)
				return dao.get_uceniks_slusa(ucenik)
		except:
			return None
		finally:
			DAOManager.release(dao)

	@staticmethod
	def get_profesors_predmets_slusa(predmet, profesor):
		dao = None
		try:
			with session_scope() as session:
				dao = DAOManager.get_korisnik_dao(session)
				slusas = dao.get_profesors_predmets_slusa(predmet, profesor)
				return slusas
		except:
			return None
		finally:
			DAOManager.release(dao)