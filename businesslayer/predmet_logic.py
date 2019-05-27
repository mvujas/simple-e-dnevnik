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
			if dao is not None:
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
			if dao is not None:
				DAOManager.release(dao)

	@staticmethod
	def add_razreds_to_predmet(predmet, *razredi):
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
			return True
		except:
			return False
		finally:
			for dao in daos.values():
				if dao is not None:
					DAOManager.release(dao)

