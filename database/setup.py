from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import config

connection_url = '%s:///%s' % (
	config.DATABASE_ENGINE, config.DATABASE_CONNECTION_STRING)

engine = create_engine(connection_url, convert_unicode=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()

if config.DATABASE_ENGINE == 'sqlite':
	# Enforce foreign key constraint in sqlite (turned off by default)
	def _fk_pragma_on_connect(dbapi_con, con_record):
		dbapi_con.execute('pragma foreign_keys=ON')

	from sqlalchemy import event
	event.listen(engine, 'connect', _fk_pragma_on_connect)

def init_db():
	import models
	Base.metadata.create_all(bind=engine)