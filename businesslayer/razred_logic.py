from models import Razred
from database import session_scope
from dataaccesslayer import DAOManager
import traceback

class RazredLogic:
	@staticmethod
	def add_razred(godina):
		dao = None
		try:
			with session_scope() as session:
				dao = DAOManager.get_razred_dao(session)
				dao.add_razred(Razred(godina))
			return True
		except:
			return False
		finally:
			if dao is not None:
				DAOManager.release(dao)

	@staticmethod
	def get_razred_by_pk(primary_key):
		dao = None
		try:
			with session_scope() as session:
				dao = DAOManager.get_razred_dao(session)
				return dao.get_razred_by_pk(primay_key)
		except:
			return None
		finally:
			if dao is not None:
				DAOManager.release(dao)

	@staticmethod
	def get_razred_by_godina(godina):
		dao = None
		try:
			with session_scope() as session:
				dao = DAOManager.get_razred_dao(session)
				return dao.get_razred_by_godina(godina)
		except:
			return None
		finally:
			if dao is not None:
				DAOManager.release(dao)

	@staticmethod
	def get_all_razred():
		dao = None
		try:
			with session_scope() as session:
				dao = DAOManager.get_razred_dao(session)
				razredi = dao.get_all_razred()
			if razredi is None:
				return None
			else:
				return { razred.id: razred for razred in razredi}
		except:
			return None
		finally:
			if dao is not None:
				DAOManager.release(dao)

	@staticmethod
	def get_all_ucenik_from_godina(godina):
		razred = None
		if isinstance(godina, Razred):
			razred = godina
		elif not isinstance(godina, int):
			return None
		daos = {'razred': None, 'korisnik': None}
		try:
			with session_scope() as session:
				daos['razred'] = DAOManager.get_razred_dao(session)
				daos['korisnik'] = DAOManager.get_korisnik_dao(session)
				if razred is None:
					razred = daos['razred'].get_razred_by_godina(godina)
				return daos['korisnik'].get_all_ucenik_from_razred(razred)
		except:
			return None
		finally:
			for dao in daos.values():
				if dao is not None:
					DAOManager.release(dao)
