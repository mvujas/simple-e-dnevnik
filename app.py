from models import *
from data_access_layer import DAOManager
from database import init_db

init_db()

dao = DAOManager.get_korisnik_dao()
admin = Admin('pera', '')
dao.delete(admin)
print(dao.save(admin))
