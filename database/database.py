from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from core.config import DB_URL


engine = create_engine(url=DB_URL, echo=True)

Base = declarative_base()

def init_db():
    Base.metadata.create_all(engine)

@contextmanager
def session_scope():
    session = sessionmaker(bind=engine)()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

if __name__ == '__main__':
    Base.metadata.create_all(engine)