import strawberry
from typing import List, Optional
from strawberry.types import Info
from app.adapters.graphql.types import ProductoType, CrearProductoInput, ActualizarProductoInput
from app.adapters.database.repository import SQLAlchemyProductRepository
from app.application.use_cases import ProductUseCases

def get_use_cases(info: Info) -> ProductUseCases:
    """
    Helper para instanciar los casos de uso a partir de la sesión de base de datos del contexto.
    """
    db = info.context["db"]
    repository = SQLAlchemyProductRepository(db)
    return ProductUseCases(repository)

def to_graphql_type(product) -> ProductoType:
    return ProductoType(
        id=product.id,
        nombre=product.nombre,
        descripcion=product.descripcion,
        precio=product.precio
    )

@strawberry.type
class Query:
    @strawberry.field
    def obtener_productos(self, info: Info) -> List[ProductoType]:
        """
        Consulta declarativa para listar todos los productos.
        """
        try:
            use_cases = get_use_cases(info)
            productos = use_cases.listar_productos()
            return [to_graphql_type(p) for p in productos]
        except Exception as e:
            raise Exception(f"Error al obtener productos: {str(e)}")

    @strawberry.field
    def obtener_producto(self, info: Info, id: int) -> ProductoType:
        """
        Consulta declarativa para obtener un producto por su ID único.
        """
        try:
            use_cases = get_use_cases(info)
            producto = use_cases.obtener_producto(id)
            return to_graphql_type(producto)
        except ValueError as e:
            raise Exception(f"No encontrado: {str(e)}")
        except Exception as e:
            raise Exception(f"Error al obtener el producto: {str(e)}")

@strawberry.type
class Mutation:
    @strawberry.mutation
    def crear_producto(self, info: Info, input: CrearProductoInput) -> ProductoType:
        """
        Mutación declarativa para crear un nuevo producto.
        """
        try:
            use_cases = get_use_cases(info)
            producto = use_cases.crear_producto(
                nombre=input.nombre,
                descripcion=input.descripcion,
                precio=input.precio
            )
            return to_graphql_type(producto)
        except ValueError as e:
            raise Exception(f"Datos inválidos: {str(e)}")
        except Exception as e:
            raise Exception(f"Error interno al crear producto: {str(e)}")

    @strawberry.mutation
    def actualizar_producto(self, info: Info, input: ActualizarProductoInput) -> ProductoType:
        """
        Mutación declarativa para actualizar un producto existente.
        """
        try:
            use_cases = get_use_cases(info)
            producto = use_cases.actualizar_producto(
                product_id=input.id,
                nombre=input.nombre,
                descripcion=input.descripcion,
                precio=input.precio
            )
            return to_graphql_type(producto)
        except ValueError as e:
            raise Exception(f"Error de actualización: {str(e)}")
        except Exception as e:
            raise Exception(f"Error interno al actualizar producto: {str(e)}")

    @strawberry.mutation
    def eliminar_producto(self, info: Info, id: int) -> bool:
        """
        Mutación declarativa para eliminar un producto por su ID único.
        """
        try:
            use_cases = get_use_cases(info)
            return use_cases.eliminar_producto(id)
        except ValueError as e:
            raise Exception(f"Error de eliminación: {str(e)}")
        except Exception as e:
            raise Exception(f"Error interno al eliminar producto: {str(e)}")
