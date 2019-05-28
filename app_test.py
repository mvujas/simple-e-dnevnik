from database import session_scope
from models import *
from businesslayer import *
'''
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


print(PredmetLogic.add_predmet('matematika'))
print(PredmetLogic.add_predmet('srpski'))

print(KorisnikLogic.get_all_korisnik())
print(KorisnikLogic.get_all_admin())
print(KorisnikLogic.get_all_ucenik())
print(KorisnikLogic.get_all_profesor())

predmeti = PredmetLogic.get_all_predmet()

predmet = predmeti[1]

from sqlalchemy import inspect

print(inspect(predmet).detached)

with session_scope() as session:
	session.add(predmet)
	print(inspect(predmet).detached)

print(inspect(predmet).detached)

from dataaccesslayer import DAOManager

razred = RazredLogic.get_razred_by_godina(5)
print(PredmetLogic.add_razreds_to_predmet(predmet, 1, 2, 3, 4, 8, 8))


print(PredmetLogic.add_predmet('matematika'))
print(PredmetLogic.add_predmet('srpski jezik'))

predmeti = PredmetLogic.get_all_predmet()
predmet = predmeti[1]

print(predmeti)
print()
PredmetLogic.set_razreds_to_predmet(predmet, 1, 2, 4, 5)

for p in predmeti.values():
	print(p, p.razredi)
print()

PredmetLogic.set_razreds_to_predmet(predmet, 1, 3, 2, 2, 8)

for p in predmeti.values():
	print(p, p.razredi)


print(KorisnikLogic.get_korisnik_by_pk(2))
'''
from views import PredmetList

PredmetList()