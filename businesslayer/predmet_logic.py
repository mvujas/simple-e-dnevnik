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
					for predmet in predmeti:
						predmet.razredi.sort(key=lambda razred: razred.godina)
					return { predmet.id: predmet for predmet in predmeti }
		except:
			return None
		finally:
			DAOManager.release(dao)

	@staticmethod
	def get_predmet_by_naziv(naziv):
		dao = None
		try:
			with session_scope() as session:
				dao = DAOManager.get_predmet_dao(session)
				predmet = dao.get_predmet_by_name(naziv)
				return predmet
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
				predmet = dao.get_predmet_by_pk(primary_key)
				predmet.razredi.sort(key=lambda razred: razred.godina)
				return predmet
		except:
			return None
		finally:
			DAOManager.release(dao)

	@staticmethod
	def add_predmet_razred_relation(predmet, godina):
		daos = { 'predmet': None, 'razred': None }
		try:
			with session_scope() as session:
				daos['predmet'] = DAOManager.get_predmet_dao(session)
				daos['razred'] = DAOManager.get_razred_dao(session)
				razred = daos['razred'].get_razred_by_godina(godina)
				if razred in predmet.razredi:
					raise UpdateInfoError('Predmet se vec slusa u unetom razredu')
				daos['predmet'].add_razred_to_predmet(predmet, razred)
			return True
		except UpdateInfoError:
			raise
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