import os

class Settings:
    PROJECT_NAME: str = "Catálogo de Productos - gRPC & Gateway REST"
    PROJECT_VERSION: str = "1.0.0"
    HOST: str = "127.0.0.1"
    PORT: int = 8001               # Puerto de la pasarela REST (FastAPI)
    GRPC_PORT: int = 50051         # Puerto del servidor gRPC nativo
    GRPC_TARGET: str = "localhost:50051"

settings = Settings()
