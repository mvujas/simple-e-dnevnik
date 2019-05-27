from models import Predmet, Razred, DozvoljeniRazredi
from sqlalchemy import inspect, and_
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
		return self.session.query(Predmet).all()

	def get_predmet_by_pk(self, primary_key):
		return self.session.query(Predmet).get(primary_key)

	def get_predmet_by_name(self, name):
		return self.session.query(Predmet).filter(Predmet.naziv == name).first()

	def add_razred_to_predmet(self, predmet, razred):
		check_type(predmet, Predmet)
		check_type(razred, Razred)
		if inspect(predmet).detached:
			self.session.add(predmet)
		if razred not in predmet.razredi:
			predmet.razredi.append(razred)	

	def remove_razred_predmet_relation(self, predmet, razred):
		check_type(predmet, Predmet)
		check_type(razred, Razred)
		if inspect(predmet).detached:
			self.session.add(predmet)
		if razred in predmet.razredi:
			predmet.razredi.remove(razred)

	def update_predmet_attribute(self, predmet, attribute, new_value):
		check_type(predmet, Predmet)
		if inspect(predmet).detached:
			self.session.add(predmet)
		setattr(predmet, attribute, new_value)