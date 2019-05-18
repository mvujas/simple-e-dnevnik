from database import Session
from abc import ABC

class GeneralDAO(ABC):
	def __init__(self):
		super(GeneralDAO, self).__init__()

	def _add_entity(self, entityClass, entity):
		if not isinstance(entity, entityClass):
			raise ValueError(f'Passed entity is not an instance of {entityClass.__name__}')
		session = None
		try:
			session = Session()
			session.add(entity)
			session.flush()
			session.commit()
			session.refresh(entity)
			return True
		except Exception as e:
			if session != None:
				session.rollback()
			return False
		finally:
			if session != None:
				session.close()

	def _update_entity(self, entityClass, filterPredicate, updateDictionary):
		session = None
		try:
			session = Session()
			entityClass.query.filter(filterPredicate).update(updateDictionary, synchronize_session=False)
			session.flush()
			session.commit()
			return True
		except Exception as e:
			if session != None:
				session.rollback()
			return False
		finally:
			if session != None:
				session.close()

	def _get_all(self, baseClass, targetClass):
		if not issubclass(targetClass, baseClass):
			raise ValueError(f'Given parameter must be subclass of class {baseClass.__name__}')
		return targetClass.query.all()