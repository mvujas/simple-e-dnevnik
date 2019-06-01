from .exceptions import UpdateInfoError
from dataaccesslayer import DAOManager
from database import session_scope
from models import Predmet
from utils import check_type

class PredmetLogic:
	@staticmethod
	def add_predmet(naziv):
		dao = None
		try:
			with session_scope() as session:
				dao = DAOManager.get_predmet_dao(session)
				dao.add_predmet(Predmet(naziv))	
			return True
		except:
			return False
		finally:
			DAOManager.release(dao)

	@staticmethod
	def get_all_predmet():
		dao = None
		try:
			with session_scope() as session:
				dao = DAOManager.get_predmet_dao(session)
				predmeti = dao.get_all_predmet()
				if predmeti is None:
					return None
				else:
					return { predmet.id: predmet for predmet in predmeti }
		except:
			return None
		finally:
			DAOManager.release(dao)

	@staticmethod
	def get_predmet_by_pk(primary_key):
		dao = None
		try:
			with session_scope() as session:
				dao = DAOManager.get_predmet_dao(session)
				return dao.get_predmet_by_pk(primary_key)
		except:
			return None
		finally:
			DAOManager.release(dao)

	@staticmethod
	def set_razreds_to_predmet(predmet, *razredi):
		for razred in razredi:
			check_type(razred, int)
		razredi = list(set(razredi))
		daos = { 'predmet': None, 'razred': None }
		try:
			with session_scope() as session:
				daos['predmet'] = DAOManager.get_predmet_dao(session)
				daos['razred'] = DAOManager.get_razred_dao(session)
				for razred in razredi:
					daos['predmet'].add_razred_to_predmet(predmet, 
						daos['razred'].get_razred_by_godina(razred))
				razredi_to_remove = []
				for razred_obj in predmet.razredi:
					if razred_obj.godina not in razredi:
						razredi_to_remove.append(razred_obj)
				for razred_to_remove in razredi_to_remove:
					daos['predmet'].remove_razred_predmet_relation(predmet, razred_to_remove)
			return True
		except:
			return False
		finally:
			for dao in daos.values():
				DAOManager.release(dao)

	@staticmethod
	def change_predmet_naziv(predmet, naziv):
		dao = None
		try:
			with session_scope() as session:
				dao = DAOManager.get_predmet_dao(session)
				if dao.get_predmet_by_name(naziv) is not None:
					raise UpdateInfoError('Vec postoji predmet sa unetim imenom')
				dao.update_predmet_attribute(predmet, 'naziv', naziv)
			return True
		except UpdateInfoError:
			raise
		except:
			return False
		finally:
			DAOManager.release(dao)		