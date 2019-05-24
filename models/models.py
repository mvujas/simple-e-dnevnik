from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.schema import PrimaryKeyConstraint, ForeignKeyConstraint, UniqueConstraint

import datetime

class Korisnik(Base):
	__tablename__ = 'korisnik'

	id = Column(Integer)
	username = Column(String(30), nullable=False, index=True)
	password = Column(String(200), nullable=False)
	uloga = Column(String(20), nullable=False)

	__table_args__ = (
		PrimaryKeyConstraint(id),
		UniqueConstraint(username),
		{}
	)

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

	id = Column(Integer)

	__table_args__ = (
		ForeignKeyConstraint([id], [Korisnik.id]),
		PrimaryKeyConstraint(id),
		{}
	)

	__mapper_args__ = {
		'polymorphic_identity':'admin'
	}

	def __repr__(self):
		return f'<Admin(id={self.id}, username={self.username})>'


class Ucenik(Korisnik):
	__tablename__ = 'ucenik'

	id = Column(Integer)
	ime = Column(String(30), nullable=False)
	prezime = Column(String(30), nullable=False)

	__table_args__ = (
		ForeignKeyConstraint([id], [Korisnik.id]),
		PrimaryKeyConstraint(id),
		{}
	)

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

	id = Column(Integer)
	ime = Column(String(30), nullable=False)
	prezime = Column(String(30), nullable=False)
	predmeti = relationship('Predmet', secondary='predaje')

	__table_args__ = (
		ForeignKeyConstraint([id], [Korisnik.id]),
		PrimaryKeyConstraint(id),
		{}
	)

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

	id = Column(Integer)
	naziv = Column(String(50), nullable=False)
	profesori = relationship('Profesor', secondary='predaje')

	__table_args__ = (
		PrimaryKeyConstraint(id),
		UniqueConstraint(naziv),
		{}
	)

	def __init__(self, naziv):
		self.naziv = naziv

	def __repr__(self):
		return f'<Predmet(id={self.id}, naziv={self.naziv})>'


class Predaje(Base):
	__tablename__ = 'predaje'

	profesor_id = Column(Integer)
	predmet_id = Column(Integer)

	__table_args__ = (
		ForeignKeyConstraint([profesor_id], [Profesor.id]), # add on delete cascade
		ForeignKeyConstraint([predmet_id], [Predmet.id]), # add on delete cascade
		PrimaryKeyConstraint(profesor_id, predmet_id),
		{}
	)

	def __repr__(self):
		return f'<Predaje()>'


class Slusa(Base):
	__tablename__ = 'slusa'

	ucenik_id = Column(Integer)
	predmet_id = Column(Integer)
	predaje_profesor_id = Column(Integer)
	predaje_predmet_id = Column(Integer)

	__table_args__ = (
		ForeignKeyConstraint([ucenik_id], [Ucenik.id]), # add on delete cascade
		ForeignKeyConstraint([predmet_id], [Predmet.id]), # add on delete cascade
		ForeignKeyConstraint([predaje_profesor_id, predaje_predmet_id], [Predaje.profesor_id, Predaje.predmet_id]), # add on delete set null
		PrimaryKeyConstraint(ucenik_id, predmet_id),
		{}
	)

	def __repr__(self):
		return f'<Slusa()>'


class Ocena(Base):
	__tablename__ = 'ocena'

	slusa_ucenik_id = Column(Integer)
	slusa_predmet_id = Column(Integer)
	ocena_id = Column(Integer)
	datum = Column(Date, default=datetime.datetime.now)
	vrednost = Column(Integer, nullable=False)

	__table_args__ = (
		ForeignKeyConstraint([slusa_ucenik_id, slusa_predmet_id], [Slusa.ucenik_id, Slusa.predmet_id]), # add on delete cascade
		PrimaryKeyConstraint(slusa_ucenik_id, slusa_predmet_id, ocena_id),
		{}
	)

	def __repr__(self):
		return f'<Ocena()>'