from typing import List, Optional
from app.domain.entities import Producto
from app.domain.repositories import ProductRepository

class ProductUseCases:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def obtener_producto(self, product_id: int) -> Producto:
        product = self.repository.get_by_id(product_id)
        if not product:
            raise ValueError(f"Producto con ID {product_id} no fue encontrado.")
        return product

    def listar_productos(self) -> List[Producto]:
        return self.repository.get_all()

    def crear_producto(self, nombre: str, descripcion: Optional[str], precio: float) -> Producto:
        nuevo_producto = Producto(
            id=None,
            nombre=nombre,
            descripcion=descripcion,
            precio=precio
        )
        nuevo_producto.validar()
        return self.repository.create(nuevo_producto)

    def actualizar_producto(self, product_id: int, nombre: Optional[str], descripcion: Optional[str], precio: Optional[float]) -> Producto:
        producto_existente = self.repository.get_by_id(product_id)
        if not producto_existente:
            raise ValueError(f"Producto con ID {product_id} no existe y no se puede actualizar.")

        if nombre is not None:
            producto_existente.nombre = nombre
        if descripcion is not None:
            producto_existente.descripcion = descripcion
        if precio is not None:
            producto_existente.precio = precio

        producto_existente.validar()
        return self.repository.update(producto_existente)

    def eliminar_producto(self, product_id: int) -> bool:
        producto_existente = self.repository.get_by_id(product_id)
        if not producto_existente:
            raise ValueError(f"Producto con ID {product_id} no existe y no se puede eliminar.")
            
        return self.repository.delete(product_id)
