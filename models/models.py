from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Date, ForeignKey

import datetime

class Korisnik(Base):
	__tablename__ = 'korisnik'

	id = Column(Integer, primary_key=True)
	username = Column(String(30), nullable=False, unique=True, index=True)
	password = Column(String(200), nullable=False)
	uloga = Column(String(20), nullable=False)

	__mapper_args__ = {
		'polymorphic_identity':'korisnik',
		'polymorphic_on':uloga
    }

	def __init__(self, username, password):
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
		return f'<Admin(id={self.id}, username={self.username})>'


class Ucenik(Korisnik):
	__tablename__ = 'ucenik'

	id = Column(Integer, ForeignKey('korisnik.id'), primary_key=True)
	ime = Column(String(30), nullable=False)
	prezime = Column(String(30), nullable=False)

	__mapper_args__ = {
		'polymorphic_identity':'ucenik'
	}		

	def __init__(self, username, password, ime, prezime):
		super(Ucenik, self).__init__(username, password)
		self.ime = ime
		self.prezime = prezime

	def __repr__(self):
		return f'<Ucenik(id={self.id}, username={self.username}, ime={self.ime}, prezime={self.prezime}))>'


class Profesor(Korisnik):
	__tablename__ = 'profesor'

	id = Column(Integer, ForeignKey('korisnik.id'), primary_key=True)
	ime = Column(String(30), nullable=False)
	prezime = Column(String(30), nullable=False)

	__mapper_args__ = {
		'polymorphic_identity':'profesor'
	}

	def __init__(self, username, password, ime, prezime):
		super(Profesor, self).__init__(username, password)
		self.ime = ime
		self.prezime = prezime

	def __repr__(self):
		return f'<Profesor(id={self.id}, username={self.username}, ime={self.ime}, prezime={self.prezime})>'


class Predmet(Base):
	__tablename__ = 'predmet'

	id = Column(Integer, primary_key=True)
	naziv = Column(String(50), unique=True, nullable=False)

	def __init__(self, naziv):
		self.naziv = naziv

	def __repr__(self):
		return f'<Predmet(id={self.id}, naziv={self.naziv})>'


class Predaje(Base):
	__tablename__ = 'predaje'

	profesor_id = Column(Integer, ForeignKey('profesor.id', ondelete='CASCADE'), primary_key=True)
	predmet_id = Column(Integer, ForeignKey('predmet.id', ondelete='CASCADE'), primary_key=True)

	def __repr__(self):
		return f'<Predaje()>'


class Slusa(Base):
	__tablename__ = 'slusa'

	ucenik_id = Column(Integer, ForeignKey('ucenik.id', ondelete='CASCADE'), primary_key=True)
	predmet_id = Column(Integer, ForeignKey('predmet.id', ondelete='CASCADE'), primary_key=True)
	predaje_profesor_id = Column(Integer, ForeignKey('predaje.profesor_id', ondelete='SET NULL'))
	predaje_predmet_id = Column(Integer, ForeignKey('predaje.predmet_id', ondelete='SET NULL'))

	def __repr__(self):
		return f'<Slusa()>'

class Ocena(Base):
	__tablename__ = 'ocena'

	slusa_ucenik_id = Column(Integer, ForeignKey('slusa.ucenik_id', ondelete='CASCADE'), primary_key=True)
	slusa_predmet_id = Column(Integer, ForeignKey('slusa.predmet_id', ondelete='CASCADE'), primary_key=True)
	ocena_id = Column(Integer, primary_key=True)
	datum = Column(Date, default=datetime.datetime.now)
	vrednost = Column(Integer, nullable=False)

	def __repr__(self):
		return f'<Ocena()>'