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

	@staticmethod
	def get_predmets_avaliable_to_ucenik(ucenik):
		dao = None
		try:
			with session_scope() as session:
				dao = DAOManager.get_predmet_dao(session)
				predmeti = dao.get_predmets_avaliable_to_ucenik(ucenik)
				if predmeti is None:
					return None
				predmeti = list(filter(lambda predmet: len(predmet.profesori) > 0, predmeti))
			return predmeti
		except UpdateInfoError:
			raise
		except:
			return None
		finally:
			DAOManager.release(dao)	

	@staticmethod
	def add_ocena(ucenik, predmet, vrednost_ocene):
		check_type(ucenik, Ucenik)
		check_type(predmet, Predmet)
		if not isinstance(vreddnost_ocene, int) or vrednost_ocene < 1 or vrednost_ocene > 5:
			raise ValueError('vrednost_ocene is out of predefined domain')
		daos = {'korisnik': None, 'predmet': None}
		try:
			with session_scope() as session:
				daos['korisnik'] = DAOManager.get_korisnik_dao(session)
				daos['predmet'] = DAOManager.get_predmet_dao(session)
				slusa = daos['korisnik'].get_uceniks_predmets_slusa(ucenik, predmet)
				if slusa is None:
					raise UpdateInfoError('Ucenik ne slusa uneti predmet')
				ocena = Ocena(vrednost_ocene, slusa)
				daos['predmet'].add_ocena(ocena)
				return True
		except UpdateInfoError:
			raise
		except:
			return False
		finally:
			for dao in daos.values():
				DAOManager.release(dao)	

	@staticmethod
	def get_profesors_predmets(profesor):
		dao = None
		try:
			with session_scope() as session:
				dao = DAOManager.get_predmet_dao(session)
				predmeti = dao.get_all_predmet_connected_with_the_profesor(profesor)
				return {predmet.id: predmet for predmet in predmeti}
		except:
			return None
		finally:
			DAOManager.release(dao)