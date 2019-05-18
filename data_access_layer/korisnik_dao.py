from database import Session
from models import Korisnik, Admin, Ucenik, Profesor

from .general_dao import GeneralDAO

class KorisnikDAO(GeneralDAO):
	def __init__(self):
		super(KorisnikDAO, self).__init__()

	def add_admin(self, admin):
		return self._add_entity(Admin, admin)

	def add_ucenik(self, ucenik):
		return self._add_entity(Ucenik, ucenik)

	def add_profesor(self, profesor):
		return self._add_entity(Profesor, profesor)

	def get_korisnik_by_id(self, id):
		return Korisnik.query.get(id)

	def get_korisnik_by_username(self, username):
		return Korisnik.query.filter(Korisnik.username == username).first()

	def get_all_korisnik(self, subclass=Korisnik):
		return self._get_all(Korisnik, subclass)

	# objects aren't synchronized after update, so korisnik should do it manually
	def update_korisnik(self, korisnik, updateDictionary):
		if not isinstance(korisnik, Korisnik):
			raise ValueError(f'Passed entity is not an instance of Korisnik')
		return self._update_entity(Korisnik, Korisnik.id == korisnik.id, updateDictionary)
