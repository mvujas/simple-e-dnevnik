from database import Session
from abc import ABC

class GeneralDAO(ABC):
	def _add_update_entity(self, entityClass, entity):
		if not isinstance(entity, entityClass):
			raise ValueError(f'Passed entity is not an instance of {entityClass.__name__}')
		session = None
		try:
			session = Session()
			session.add(entity)
			session.commit()
			return True
		except Exception as e:
			if session != None:
				session.rollback()
			return False
		finally:
			if session != None:
				session.close()

	def _delete_entity(self, entityClass, entity):
		if not isinstance(entity, entityClass):
			raise ValueError(f'Passed entity is not an instance of {entityClass.__name__}')
		session = None
		try:
			session = Session()
			session.delete(entity)
			session.commit()
			return True
		except Exception as e:
			if session != None:
				session.rollback()
			return False
		finally:
			if session != None:
				session.close()