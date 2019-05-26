from models import Razred, Ucenik

from .general_dao import GeneralDAO
from utils import check_type

class RazredDAO(GeneralDAO):
	def add_razred(self, razred):
		check_type(razred, Razred)
		self.session.add(razred)

	def delete_razred(self, razred):
		check_type(razred, Razred)
		self.session.delete(razred)

	def get_all_razred(self):
		return self.session.query(Razred).all()

	def get_razred_by_pk(self, primary_key):
		return self.session.query(Razred).get(primary_key)

	def get_razred_by_godina(self, godina):
		return self.session.query(Razred).filter(Razred.godina == godina).first()