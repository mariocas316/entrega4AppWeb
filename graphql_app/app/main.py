import uvicorn
from app.infrastructure.config import settings

if __name__ == "__main__":
    # Arrancamos Uvicorn apuntando a la instancia 'app' en el módulo 'web' de la capa de infraestructura
    print(f"Iniciando el servidor de GraphQL en http://{settings.HOST}:{settings.PORT}")
    print(f"Playground interactivo GraphiQL disponible en http://{settings.HOST}:{settings.PORT}/graphql")
    uvicorn.run(
        "app.infrastructure.web:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )
