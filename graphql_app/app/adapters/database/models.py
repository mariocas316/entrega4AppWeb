from sqlalchemy import Column, Integer, String, Float
from app.adapters.database.connection import Base

class ProductoDB(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String, nullable=True)
    precio = Column(Float, nullable=False)
