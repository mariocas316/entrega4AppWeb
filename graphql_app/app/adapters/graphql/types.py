import strawberry
from typing import Optional

@strawberry.type
class ProductoType:
    id: int
    nombre: str
    descripcion: Optional[str]
    precio: float

@strawberry.input
class CrearProductoInput:
    nombre: str
    descripcion: Optional[str] = None
    precio: float

@strawberry.input
class ActualizarProductoInput:
    id: int
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
