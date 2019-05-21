from database import Session
from models import Korisnik, Admin, Ucenik, Profesor

from .general_dao import GeneralDAO

class KorisnikDAO(GeneralDAO):
	def __init__(self):
		super(KorisnikDAO, self).__init__()

	def save(self, korisnik):
		return self._add_update_entity(korisnik, Korisnik)

	def delete(self, korisnik):
		return self._delete_entity(korisnik, Korisnik)