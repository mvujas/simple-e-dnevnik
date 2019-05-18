from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class Korisnik(Base):
	__tablename__ = 'korisnik'

	id = Column(Integer, primary_key=True)
	ime = Column(String(30))
	prezime = Column(String(30))
	username = Column(String(30), nullable=False, unique=True, index=True)
	password = Column(String(200), nullable=False)
	uloga = Column(String(20), nullable=False)

	__mapper_args__ = {
		'polymorphic_identity':'korisnik',
		'polymorphic_on':uloga
    }

	def __init__(self, ime, prezime, username, password):
		self.ime = ime
		self.prezime = prezime
		self.username = username
		self.password = password

	def __repr__(self):
		return f'<Korisnik(id={self.id}, username={self.username})>'


class Admin(Korisnik):
	__tablename__ = 'admin'

	id = Column(Integer, ForeignKey('korisnik.id'), primary_key=True)

	__mapper_args__ = {
		'polymorphic_identity':'admin'
	}		

	def __repr__(self):
		return f'<Admin()>'


class Ucenik(Korisnik):
	__tablename__ = 'ucenik'

	id = Column(Integer, ForeignKey('korisnik.id'), primary_key=True)

	__mapper_args__ = {
		'polymorphic_identity':'ucenik'
	}

	def __repr__(self):
		return f'<Ucenik()>'


class Profesor(Korisnik):
	__tablename__ = 'profesor'

	id = Column(Integer, ForeignKey('korisnik.id'), primary_key=True)

	__mapper_args__ = {
		'polymorphic_identity':'profesor'
	}

	def __repr__(self):
		return f'<Profesor()>'