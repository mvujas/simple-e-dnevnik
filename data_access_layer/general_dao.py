from database import Session
from abc import ABC
from utils import debug_print

class GeneralDAO(ABC):
	def _add_update_entity(self, entity, *entityClasses):
		if len(entityClasses) > 0 and not any(
				map(lambda entityClass: isinstance(entity, entityClass), entityClasses)):
			raise ValueError(f'Passed entity is not an instance of any of given entity classes')
		session = None
		try:
			session = Session()
			session.add(entity)
			session.commit()
			return True
		except Exception as e:
			if session != None:
				session.rollback()
			debug_print('Exception(_add_update_entity) =', e)
			return False
		finally:
			if session != None:
				session.close()

	def _delete_entity(self, entity, *entityClasses):
		if len(entityClasses) > 0 and not any(
				map(lambda entityClass: isinstance(entity, entityClass), entityClasses)):
			raise ValueError(f'Passed entity is not an instance of any of given entity classes')
		session = None
		try:
			session = Session()
			session.delete(entity)
			session.commit()
			return True
		except Exception as e:
			if session != None:
				session.rollback()
			debug_print('Exception(_delete_entity) =', e)
			return False
		finally:
			if session != None:
				session.close()