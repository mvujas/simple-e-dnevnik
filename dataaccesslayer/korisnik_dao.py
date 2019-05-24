from models import Korisnik, Admin, Ucenik, Profesor

from .general_dao import GeneralDAO
from utils import check_type

class KorisnikDAO(GeneralDAO):
	def add_korisnik(self, korisnik):
		check_type(korisnik, Korisnik)
		self.session.add(korisnik)

	def delete_korisnik(self, korisnik):
		check_type(korisnik, Korisnik)
		self.session.delete(korisnik)

	def get_korisnik_by_pk(self, primary_key):
		return self.session.query(Korisnik).get(primary_key)

	def get_korisnik_by_username(self, username):
		return self.session.query(Korisnik).filter(Korisnik.username == username).first() 

	def get_all_korisnik(self):
		return self.session.query(Korisnik).all()