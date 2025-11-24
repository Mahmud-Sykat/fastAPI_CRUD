from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# MySQL connection string
DATABASE_URL = "mysql+pymysql://root:@127.0.0.1:3306/test"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
