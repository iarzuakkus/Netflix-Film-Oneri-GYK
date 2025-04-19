from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# PostgreSQL bağlantı bilgileri
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "12345"
POSTGRES_SERVER = "localhost"
POSTGRES_PORT = "5432"
POSTGRES_DB = "netflix"

# SQLAlchemy veritabanı URL'si
SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Veritabanı motoru oluştur
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal sınıfı oluştur
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base sınıfı
Base = declarative_base()

# Veritabanı bağlantısı için dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 