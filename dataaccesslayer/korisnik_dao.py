from models import *
from sqlalchemy import inspect, and_
from sqlalchemy.orm import joinedload
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

	def get_all_ucenik(self):
		return self.session.query(Ucenik).options(joinedload(Ucenik.razred)).all()

	def get_all_profesor(self):
		return self.session.query(Profesor).options(joinedload(Profesor.predmeti)).all()

	def get_all_ucenik_from_razred(self, razred):
		check_type(razred, Razred)
		return self.session.query(Ucenik).options(joinedload(Ucenik.razred)).filter(Ucenik.razred_id == razred.id).all()

	def get_ucenik_by_pk(self, primary_key):
		return self.session.query(Ucenik).options(joinedload(Ucenik.razred)).get(primary_key)

	def get_profesor_by_pk(self, primary_key):
		return self.session.query(Profesor).options(joinedload(Profesor.predmeti)).get(primary_key)

	def update_korisnik_attribute(self, korisnik, attribute, new_value):
		check_type(korisnik, Korisnik)
		if inspect(korisnik).detached:
			self.session.add(korisnik)
		setattr(korisnik, attribute, new_value)

	def add_predmet_to_profesor(self, profesor, predmet):
		check_type(profesor, Profesor)
		check_type(predmet, Predmet)
		self.session.add(Predaje(profesor, predmet))

	def add_predmet_to_ucenik(self, ucenik, predmet, profesor):
		check_type(ucenik, Ucenik)
		check_type(predmet, Predmet)
		check_type(profesor, Profesor)
		self.session.add(Slusa(ucenik, predmet, profesor))

	def get_uceniks_slusa(self, ucenik):
		check_type(ucenik, Ucenik)
		return self.session.query(Slusa).filter(Slusa.ucenik_id == ucenik.id).all()

	def get_uceniks_predmets_slusa(self, ucenik, predmet):
		check_type(ucenik, Ucenik)
		check_type(predmet, Predmet)
		return (
			self.session.query(Slusa).filter(
				and_(
					Slusa.predmet_id == predmet.id,
					Slusa.ucenik_id == ucenik.id
				)
			).first()
		)

	def does_slusa_exists(self, ucenik, predmet):
		return self.get_uceniks_predmets_slusa(ucenik, predmet) is not None

	def get_profesors_predmets_slusa(self, predmet, profesor):
		check_type(predmet, Predmet)
		check_type(profesor, Profesor)
		return (
			self.session.query(Slusa).filter(
				and_(
					Slusa.predaje_predmet_id == predmet.id,
					Slusa.predaje_profesor_id == profesor.id
				)
			).all()
		)

	def get_predaje(self, predmet, profesor):
		check_type(predmet, Predmet)
		check_type(profesor, Profesor)
		return (
			self.session.query(Predaje).filter(
				and_(
					Predaje.predmet_id == predmet.id,
					Predmet.profesor_id == profesor.id
				)
			).first()
		)

	def get_slusa_by_pk(self, ucenik_id, predmet_id):
		check_type(ucenik_id, int)
		check_type(predmet_id, int)
		return (
			self.session.query(Slusa).filter(
				and_(
					Slusa.ucenik_id == ucenik_id,
					Slusa.predmet_id == predmet_id
				)
			).first()
		)