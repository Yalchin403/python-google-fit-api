from apps.conf import get_settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SETTINGS = get_settings()
engine = create_engine(
    SETTINGS.DATABASE_URL, connect_args={"check_same_thread": False}
)
Base = declarative_base()


# safe context manager for db
class DBSession:
    def __init__(self):
        engine = create_engine(SETTINGS.DATABASE_URL)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
