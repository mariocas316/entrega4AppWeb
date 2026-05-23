from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./products.db"

# engine con check_same_thread=False para SQLite en ambientes multihilo
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Función generadora para inyectar la sesión de base de datos de forma segura.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
