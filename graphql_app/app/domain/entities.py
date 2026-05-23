from dataclasses import dataclass
from typing import Optional

@dataclass
class Producto:
    id: Optional[int]
    nombre: str
    descripcion: Optional[str]
    precio: float

    def validar(self) -> None:
        """
        Valida las reglas de negocio del producto.
        """
        if not self.nombre or self.nombre.strip() == "":
            raise ValueError("El nombre del producto no puede estar vacío.")
        if self.precio < 0:
            raise ValueError("El precio del producto no puede ser negativo.")
