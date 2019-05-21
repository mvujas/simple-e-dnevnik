from models import *
from data_access_layer import KorisnikDAO
from database import init_db, Session, engine

init_db()
'''
dao = KorisnikDAO()

admin = models.Admin('pera', 'maliPerica')

print(admin)
print(dao.add_admin(admin))
print(admin)

print(dao.update_korisnik(admin, {
	models.Korisnik.username: 'pera11'
}))

print(admin)
print(dao.add_ucenik(models.Ucenik('pera11', 'perica', 'Pera', 'Peric')))

print(models.Korisnik.query.all())

print(dao.get_all_korisnik(models.Admin))
'''


session = Session()

mat = Predmet('matematika')
prof = Profesor('perica', '', 'Pera', 'Peric')
admin = Admin('admin', 'admin123')
ucenik = Ucenik('marica', '', 'Mara', 'Maric')
#profMat = Predaje(prof, mat)

lista = [mat, prof, admin, ucenik]

print('Pre add_all: ', lista)
session.add_all(lista)
session.commit()
print('Posle add_all: ', lista)

admin2 = Admin('admin2', '')
session.add(admin2)
session.commit()
print('Posle delete: ', admin2)
session.close()

prof.ime = 'Misa'
session1 = Session()
session1.delete(prof)
session1.commit()

for row in session1.execute('pragma foreign_keys;'):
	print(row)