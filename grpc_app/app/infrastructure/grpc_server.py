import asyncio
import grpc
from app.adapters.grpc.generated import product_pb2_grpc
from app.adapters.grpc.controllers import ProductServiceServicer
from app.infrastructure.config import settings
from app.adapters.database.connection import engine
from app.adapters.database.models import Base

# Creamos las tablas de SQLite para gRPC al arrancar la infraestructura
Base.metadata.create_all(bind=engine)

class GRPCServer:
    def __init__(self):
        self.server = None

    async def start(self) -> None:
        """
        Inicializa y arranca de forma asíncrona el servidor gRPC nativo.
        """
        self.server = grpc.aio.server()
        
        # Registramos el controlador (Servicer) en el servidor gRPC
        product_pb2_grpc.add_ProductServiceServicer_to_server(
            ProductServiceServicer(),
            self.server
        )
        
        # Enlazamos la dirección de escucha (IPv4/IPv6 wildcard) en el puerto por defecto (50051)
        listen_addr = f"[::]:{settings.GRPC_PORT}"
        self.server.add_insecure_port(listen_addr)
        
        await self.server.start()
        print(f"==================================================")
        print(f" Servidor gRPC nativo iniciado en {listen_addr}")
        print(f"==================================================")

    async def stop(self) -> None:
        """
        Detiene de forma limpia el servidor gRPC liberando puertos.
        """
        if self.server:
            print("Deteniendo el servidor gRPC nativo...")
            await self.server.stop(grace=5)
            print("Servidor gRPC detenido exitosamente.")
