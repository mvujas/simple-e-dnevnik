from models import *
from data_access_layer import DAOManager
from database import init_db, session_scope

init_db()


try :
	with session_scope() as session:
		dao = DAOManager.get_korisnik_dao(session)
		dao.add(Admin('a', ''))
		dao.add(Ucenik('pera', '', 'Pera', 'Peric'))
		print(dao.get_by_username('b'))
		print(dao.get_by_username('a'))
		print(dao.get_all())
		DAOManager.release(dao)
except:
	print('Greska')