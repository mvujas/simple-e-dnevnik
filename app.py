from database import init_db
from businesslayer import KorisnikLogic

init_db()
print(KorisnikLogic.register_user(username='pera', password='Milos123', uloga='ucenik', ime='  Pera', prezime='   Peric '))
print(KorisnikLogic.register_user(username='pera1', password='Milos123', uloga='ucenik', ime='  Pera', prezime='   Peric '))
print(KorisnikLogic.register_user(username='admin', password='admin12345', uloga='admin'))
print(KorisnikLogic.register_user(username='vasa', password='profa1111', uloga='profesor', ime='  Vasa', prezime='   Vesic '))

from views import main_view

main_view()