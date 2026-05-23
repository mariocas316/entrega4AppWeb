from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities import Producto

class ProductRepository(ABC):
    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Producto]:
        """
        Obtiene un producto por su ID.
        """
        pass

    @abstractmethod
    def get_all(self) -> List[Producto]:
        """
        Obtiene todos los productos.
        """
        pass

    @abstractmethod
    def create(self, product: Producto) -> Producto:
        """
        Crea un nuevo producto en el repositorio.
        """
        pass

    @abstractmethod
    def update(self, product: Producto) -> Producto:
        """
        Actualiza un producto existente en el repositorio.
        """
        pass

    @abstractmethod
    def delete(self, product_id: int) -> bool:
        """
        Elimina un producto por su ID.
        """
        pass
