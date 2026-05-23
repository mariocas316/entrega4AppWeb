import asyncio
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.infrastructure.config import settings
from app.infrastructure.grpc_server import GRPCServer
from app.infrastructure.web_gateway import app as gateway_app

# Instanciamos el manejador del ciclo de vida del servidor gRPC
grpc_server = GRPCServer()

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    """
    Manejador del ciclo de vida de FastAPI que arranca el servidor gRPC nativo 
    de manera asíncrona en segundo plano y lo apaga ordenadamente al cerrar el Gateway.
    """
    # Iniciamos el servidor gRPC en el loop de eventos asíncronos activo de FastAPI
    asyncio.create_task(grpc_server.start())
    
    yield  # La aplicación corre aquí
    
    # Apagado ordenado
    await grpc_server.stop()

# Asignamos el lifespan al gateway_app
gateway_app.router.lifespan_context = app_lifespan

if __name__ == "__main__":
    print(f"==================================================")
    print(f" Iniciando la Pasarela REST en http://{settings.HOST}:{settings.PORT}")
    print(f" Servidor gRPC ejecutándose en puerto {settings.GRPC_PORT}")
    print(f"==================================================")
    
    uvicorn.run(
        "app.main:gateway_app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )
