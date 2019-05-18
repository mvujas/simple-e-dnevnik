import models
from data_access_layer import KorisnikDAO
from database import init_db

init_db()

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