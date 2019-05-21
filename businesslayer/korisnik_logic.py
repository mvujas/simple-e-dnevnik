from dataaccesslayer import DAOManager
from utils import debug_print
from models import *
from database import session_scope
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
		if len(password) < config.MINIMUM_USERNAME_LENGTH:
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
					korisnik = Ucenik(username, password, ime, prezime)
		except InvalidKorisnikInfoError:
			raise
		except:
			debug_print('Insufficient params passed to register_user\n', traceback.format_exc())
			return False

		try:
			with session_scope() as session:
				dao = DAOManager.get_korisnik_dao(session)
				if dao.get_by_username(korisnik.username) is not None:
					raise InvalidKorisnikInfoError('Vec postoji korisnik sa datim username-om')
				dao.add(korisnik)
			return True
		except InvalidKorisnikInfoError:
			raise
		except:
			return False

	@staticmethod
	def authenticate_user(username, password):
		try:
			username = username.strip()
			password = password.strip()
			with session_scope() as session:
				dao = DAOManager.get_korisnik_dao(session)
				user = dao.get_by_username(username)
				if user is None:
					return None
				if bcrypt.checkpw(password.encode(), user.password):
					session.refresh(user)
					return user
				else:
					return None
		except:
			return None
