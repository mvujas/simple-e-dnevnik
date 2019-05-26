from dataaccesslayer import DAOManager
from utils import debug_print
from models import *
from database import session_scope
from .razred_logic import RazredLogic
import traceback
import bcrypt
import config
import re


class InvalidKorisnikInfoError(Exception):
	pass

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
			if dao is not None:
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
			if dao is not None:
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
			if dao is not None:
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
			if dao is not None:
				DAOManager.release(dao)