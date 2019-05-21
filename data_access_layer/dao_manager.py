from .korisnik_dao import KorisnikDAO

class DAOManager:
	__daos = {
		'KorisnikDAO': KorisnikDAO()
	}

	@classmethod
	def __get_dao(cls, dao_name):
		if not dao_name in cls.__daos:
			raise ValueError('There is no such DAO')
		return cls.__daos[dao_name]

	@classmethod
	def get_korisnik_dao(cls):
		return cls.__get_dao('KorisnikDAO')