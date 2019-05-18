import models
import data_access_layer as dao
from database import init_db

init_db()

print(dao.add_entity(models.Admin(None, None, 'mvujas', 'maliSvet')))
print(dao.add_entity(models.Ucenik('Pera', 'Peric', 'perica', 'maliii')))
