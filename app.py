from models import *
from data_access_layer import DAOManager
from database import init_db, session_scope

init_db()

with session_scope() as session:
	session.add(Admin('pera', 'pera123'))