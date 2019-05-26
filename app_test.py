from database import session_scope
from models import *
from businesslayer import *
'''
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


print(KorisnikLogic.register_user(username='ABCD1',password='admin12345',ime='ab',prezime='be',uloga='ucenik',razred=5))
print(KorisnikLogic.register_user(username='ABCD2',password='admin12345',ime='ab',prezime='be',uloga='ucenik',razred=4))
print(KorisnikLogic.register_user(username='ABCD3',password='admin12345',ime='ab',prezime='be',uloga='ucenik',razred=4))

razredi = RazredLogic.get_all_razred()

print(razredi)

print(RazredLogic.get_all_ucenik_from_godina(5))
print(RazredLogic.get_all_ucenik_from_godina(4))
print(RazredLogic.get_all_ucenik_from_godina(3))

print(RazredLogic.get_razred_by_godina(1))
print(RazredLogic.get_razred_by_godina(2))
print(RazredLogic.get_razred_by_godina(3))
print(RazredLogic.get_razred_by_godina(4))

print(RazredLogic.get_razred_by_pk(5))
print(RazredLogic.get_razred_by_pk(6))
print(RazredLogic.get_razred_by_pk(7))
print(RazredLogic.get_razred_by_pk(8))
'''

m = Predmet('matematika')
s = Predmet('srpski jezik')

razredi = RazredLogic.get_all_razred()

with session_scope() as session:
	session.add_all([m, s])

	for i in range(1,5):
		m.razredi.append(razredi[i])
	for i in range(4,7):
		s.razredi.append(razredi[i])