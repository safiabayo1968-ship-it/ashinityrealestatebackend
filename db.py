from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from ashinity.core.config import settings

# Use psycopg2 for sync connections
db_url = settings.DATABASE_URL  # should be postgresql+psycopg2://...

engine = create_engine(db_url, echo=False)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)

Base = declarative_base()

# Dependency function
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
