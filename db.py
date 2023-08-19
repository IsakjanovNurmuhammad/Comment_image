from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base



SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Mum1989$@localhost:5432/messsenger"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


def get_db():
    global db
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
