from models import *
from database import Session

def add_entity(entity):
	session = None
	try:
		session = Session()
		session.add(entity)
		session.flush()
		session.commit()
		return True
	except Exception as e:
		if session != None:
			session.rollback()
		print(e)
		return False
	finally:
		if session != None:
			session.close