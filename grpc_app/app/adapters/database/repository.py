from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.entities import Producto
from app.domain.repositories import ProductRepository
from app.adapters.database.models import ProductoDB

class SQLAlchemyProductRepository(ProductRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_domain(self, db_product: ProductoDB) -> Producto:
        return Producto(
            id=db_product.id,
            nombre=db_product.nombre,
            descripcion=db_product.descripcion,
            precio=db_product.precio
        )

    def _to_db(self, domain_product: Producto) -> ProductoDB:
        return ProductoDB(
            id=domain_product.id,
            nombre=domain_product.nombre,
            descripcion=domain_product.descripcion,
            precio=domain_product.precio
        )

    def get_by_id(self, product_id: int) -> Optional[Producto]:
        db_product = self.db.query(ProductoDB).filter(ProductoDB.id == product_id).first()
        if db_product:
            return self._to_domain(db_product)
        return None

    def get_all(self) -> List[Producto]:
        db_products = self.db.query(ProductoDB).all()
        return [self._to_domain(p) for p in db_products]

    def create(self, product: Producto) -> Producto:
        db_product = self._to_db(product)
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return self._to_domain(db_product)

    def update(self, product: Producto) -> Producto:
        db_product = self.db.query(ProductoDB).filter(ProductoDB.id == product.id).first()
        if db_product:
            db_product.nombre = product.nombre
            db_product.descripcion = product.descripcion
            db_product.precio = product.precio
            self.db.commit()
            self.db.refresh(db_product)
            return self._to_domain(db_product)
        raise ValueError(f"No se pudo encontrar el producto con ID {product.id} para actualizar.")

    def delete(self, product_id: int) -> bool:
        db_product = self.db.query(ProductoDB).filter(ProductoDB.id == product_id).first()
        if db_product:
            self.db.delete(db_product)
            self.db.commit()
            return True
        return False
