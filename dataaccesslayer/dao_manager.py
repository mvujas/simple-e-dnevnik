from .korisnik_dao import KorisnikDAO
from utils.datatypes import ObjectPool

class DAOManager:
	__daos = {
		KorisnikDAO: ObjectPool(KorisnikDAO)
	}

	@classmethod
	def __get_dao(cls, dao_type, session):
		try:
			dao_object = cls.__daos[dao_type].get()
			dao_object.session = session
			return dao_object
		except:
			raise ValueError('There is no such DAO')

	@classmethod
	def get_korisnik_dao(cls, session):
		return cls.__get_dao(KorisnikDAO, session)

	@classmethod
	def release(cls, dao_object):
		try:
			cls.__daos[type(dao_object)].release(dao_object)
		except:
			raise ValueError('Error occured during release of DAO')