from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import config

engine = create_engine('sqlite:///%s' % config.DATABASE, convert_unicode=True)
Session = scoped_session(sessionmaker(autocommit=False,
										autoflush=False,
										bind=engine))
Base = declarative_base()
Base.query = Session.query_property()

def init_db():
	import models
	Base.metadata.create_all(bind=engine)