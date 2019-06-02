from models import *
from sqlalchemy import inspect, and_, func
from sqlalchemy.orm import joinedload
from .general_dao import GeneralDAO
from utils import check_type

class PredmetDAO(GeneralDAO):
	def add_predmet(self, predmet):
		check_type(predmet, Predmet)
		self.session.add(predmet)

	def delete_predmet(self, predmet):
		check_type(predmet, Predmet)
		self.session.delete(predmet)

	def get_all_predmet(self):
		return self.session.query(Predmet).options(joinedload(Predmet.razredi)).all()

	def get_predmet_by_pk(self, primary_key):
		return self.session.query(Predmet).options(joinedload(Predmet.razredi)).get(primary_key)

	def get_predmet_by_name(self, name):
		return (
			self.session
			.query(Predmet)
			.options(joinedload(Predmet.razredi))
			.filter(func.lower(Predmet.naziv) == func.lower(name))
			.first()
		)

	def __get_all_predmet_ids_connected_with_profesor(self, profesor):
		return (
			self.session
			.query(Predaje.predmet_id)
			.filter(Predaje.profesor_id == profesor.id)
			.all()
		)

	def get_all_predmet_connected_with_the_profesor(self, profesor):
		check_type(profesor, Profesor)
		assert profesor.id != None
		predmet_ids = list(map(lambda id: id[0], self.__get_all_predmet_ids_connected_with_profesor(profesor)))
		return (
			self.session
			.query(Predmet)
			.filter(
				Predmet.id.in_(predmet_ids)
			)
			.all()
		)

	def get_all_predmet_not_connected_with_the_profesor(self, profesor):
		check_type(profesor, Profesor)
		assert profesor.id != None
		return (
			self.session
			.query(Predmet)
			.filter(
				Predmet.id.notin_(self.__get_all_predmet_ids_connected_with_profesor(profesor))
			)
			.all()
		)

	def add_razred_to_predmet(self, predmet, razred):
		check_type(predmet, Predmet)
		check_type(razred, Razred)
		self.session.add(DozvoljeniRazredi(razred, predmet))

	def update_predmet_attribute(self, predmet, attribute, new_value):
		check_type(predmet, Predmet)
		if inspect(predmet).detached:
			if predmet.id is not None:
				predmet = self.get_predmet_by_pk(predmet.id)
			else:
				self.session.add(predmet)
		setattr(predmet, attribute, new_value)

	def __get_predmet_ids_in_uceniks_slusa(self, ucenik):
		check_type(ucenik, Ucenik)
		return (
			self.session
			.query(Slusa.predmet_id)
			.filter(Slusa.ucenik_id == ucenik.id)
			.all()
		)

	def get_predmets_avaliable_to_ucenik(self, ucenik):
		check_type(ucenik, Ucenik)
		not_targeted_ids = list(map(lambda id: id[0], self.__get_predmet_ids_in_uceniks_slusa(ucenik)))
		return (
			self.session
			.query(Predmet)
			.distinct(Predmet.id)
			.options(joinedload(Predmet.profesori))
			.join(DozvoljeniRazredi)
			.filter(
				and_(
					and_(
						Predmet.id == DozvoljeniRazredi.predmet_id,
						DozvoljeniRazredi.razred_id == ucenik.razred_id
					),
					Predmet.id.notin_(not_targeted_ids)
				)
			).all()
		)

	def add_ocena(self, ocena):
		check_type(ocena, Ocena)
		self.session.add(ocena)