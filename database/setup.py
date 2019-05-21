from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import config

engine = create_engine(config.DATABASE_CONNECTION_STRING, convert_unicode=True)
Session = sessionmaker(bind=engine, expire_on_commit=True)
Base = declarative_base()

if config.DATABASE_ENGINE == 'sqlite':
	# Enforce foreign key constraint in sqlite (turned off by default)
	def _fk_pragma_on_connect(dbapi_con, con_record):
		dbapi_con.execute('pragma foreign_keys=ON')

	from sqlalchemy import event
	event.listen(engine, 'connect', _fk_pragma_on_connect)


from contextlib import contextmanager
from utils import debug_print
import traceback

@contextmanager
def session_scope():
	session = Session()
	try:
		yield session
		session.commit()
	except:
		session.rollback()
		debug_print('session_scope exception =', traceback.format_exc())
		raise
	finally:
		session.close()


def init_db():
	import models
	Base.metadata.create_all(bind=engine)