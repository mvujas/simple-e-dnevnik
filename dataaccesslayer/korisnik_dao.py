from models import Korisnik, Admin, Ucenik, Profesor, Razred
from sqlalchemy import inspect
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

	def get_all_ucenik_from_razred(self, razred):
		check_type(razred, Razred)
		return self.session.query(Ucenik).filter(Ucenik.razred_id == razred.id).all()

	def update_korisnik_attribute(self, korisnik, attribute, new_value):
		check_type(korisnik, Korisnik)
		if inspect(korisnik).detached:
			self.session.add(korisnik)
		setattr(korisnik, attribute, new_value)

	def get_all_korisnik_from_subclass(self, subclass):
		if not issubclass(subclass, Korisnik):
			return ValueError('Passed class must be subclass of Korisnik')
		return self.session.query(subclass).all()