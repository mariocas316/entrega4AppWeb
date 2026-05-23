import grpc
from app.adapters.grpc.generated import product_pb2
from app.adapters.grpc.generated import product_pb2_grpc
from app.adapters.database.connection import SessionLocal
from app.adapters.database.repository import SQLAlchemyProductRepository
from app.application.use_cases import ProductUseCases

class ProductServiceServicer(product_pb2_grpc.ProductServiceServicer):
    
    def _to_protobuf(self, product) -> product_pb2.ProductResponse:
        return product_pb2.ProductResponse(
            id=product.id,
            nombre=product.nombre,
            descripcion=product.descripcion or "",
            precio=product.precio
        )

    async def CreateProduct(self, request, context):
        """
        Crear un producto a través de gRPC.
        """
        try:
            with SessionLocal() as db:
                repo = SQLAlchemyProductRepository(db)
                use_cases = ProductUseCases(repo)
                
                # Ejecutamos el caso de uso
                producto = use_cases.crear_producto(
                    nombre=request.nombre,
                    descripcion=request.descripcion if request.descripcion else None,
                    precio=request.precio
                )
                return self._to_protobuf(producto)
        except ValueError as e:
            # Error de validación (ej. precio negativo)
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, f"Datos inválidos: {str(e)}")
        except Exception as e:
            await context.abort(grpc.StatusCode.INTERNAL, f"Error interno en gRPC: {str(e)}")

    async def GetProduct(self, request, context):
        """
        Obtener un producto por ID a través de gRPC.
        """
        try:
            with SessionLocal() as db:
                repo = SQLAlchemyProductRepository(db)
                use_cases = ProductUseCases(repo)
                
                producto = use_cases.obtener_producto(request.id)
                return self._to_protobuf(producto)
        except ValueError as e:
            await context.abort(grpc.StatusCode.NOT_FOUND, str(e))
        except Exception as e:
            await context.abort(grpc.StatusCode.INTERNAL, f"Error al buscar producto: {str(e)}")

    async def ListProducts(self, request, context):
        """
        Listar todos los productos en tiempo real.
        """
        try:
            with SessionLocal() as db:
                repo = SQLAlchemyProductRepository(db)
                use_cases = ProductUseCases(repo)
                
                productos = use_cases.listar_productos()
                return product_pb2.ListProductsResponse(
                    productos=[self._to_protobuf(p) for p in productos]
                )
        except Exception as e:
            await context.abort(grpc.StatusCode.INTERNAL, f"Error al listar productos: {str(e)}")

    async def UpdateProduct(self, request, context):
        """
        Actualizar un producto existente.
        """
        try:
            with SessionLocal() as db:
                repo = SQLAlchemyProductRepository(db)
                use_cases = ProductUseCases(repo)
                
                # Manejamos opcionales de proto3 para inyección correcta
                nombre = request.nombre if request.HasField("nombre") else None
                descripcion = request.descripcion if request.HasField("descripcion") else None
                precio = request.precio if request.HasField("precio") else None
                
                producto = use_cases.actualizar_producto(
                    product_id=request.id,
                    nombre=nombre,
                    descripcion=descripcion,
                    precio=precio
                )
                return self._to_protobuf(producto)
        except ValueError as e:
            await context.abort(grpc.StatusCode.NOT_FOUND, str(e))
        except Exception as e:
            await context.abort(grpc.StatusCode.INTERNAL, f"Error al actualizar producto: {str(e)}")

    async def DeleteProduct(self, request, context):
        """
        Eliminar un producto por su ID.
        """
        try:
            with SessionLocal() as db:
                repo = SQLAlchemyProductRepository(db)
                use_cases = ProductUseCases(repo)
                
                success = use_cases.eliminar_producto(request.id)
                return product_pb2.DeleteProductResponse(
                    success=success,
                    message=f"Producto con ID {request.id} eliminado correctamente."
                )
        except ValueError as e:
            await context.abort(grpc.StatusCode.NOT_FOUND, str(e))
        except Exception as e:
            await context.abort(grpc.StatusCode.INTERNAL, f"Error al eliminar producto: {str(e)}")
