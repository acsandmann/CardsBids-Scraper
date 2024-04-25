from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("sqlite:///./cars.db", echo=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def init_db(Base):
    Base.metadata.bind = engine
    Base.metadata.create_all(bind=engine)