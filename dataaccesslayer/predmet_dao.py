from models import Predmet

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
		return self.session(Predmet).all()

	def get_predmet_by_pk(self, primary_key):
		return self.session(Predmet).get(primary_key)