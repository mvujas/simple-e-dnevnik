from database import init_db
from businesslayer import KorisnikLogic

init_db()
print(KorisnikLogic.register_user(username='pera', password='Milos123', uloga='ucenik', ime='  Pera', prezime='   Peric '))
print(KorisnikLogic.register_user(username='pera', password='Milos123', uloga='ucenik', ime='  Pera', prezime='   Peric '))
user = KorisnikLogic.authenticate_user(username='pera', password='  Milos123')
print(user)