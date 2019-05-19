from database import Session
from models import Korisnik, Admin, Ucenik, Profesor

from .general_dao import GeneralDAO

class KorisnikDAO(GeneralDAO):
	def __init__(self):
		super(KorisnikDAO, self).__init__()

	# Iako su add i update identicne metode, blize je relacionom modelu, pa da ne bi zbunjivalo
	def add(self, korisnik):
		return self._add_update_entity(Korisnik, korisnik)

	def update(self, korisnik):
		return self._add_update_entity(Korisnik, korisnik)

	def delete(self, korisnik):
		return self._delete_entity(Korisnik, Korisnik)