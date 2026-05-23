from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
import strawberry
from strawberry.fastapi import GraphQLRouter

from app.infrastructure.config import settings
from app.adapters.database.connection import engine, get_db
from app.adapters.database.models import Base
from app.adapters.graphql.resolvers import Query, Mutation

# Crear tablas en SQLite en el arranque (lifespan o startup)
Base.metadata.create_all(bind=engine)

# Crear el esquema Strawberry GraphQL
schema = strawberry.Schema(query=Query, mutation=Mutation)

# Generar contexto de base de datos para los resolvers de GraphQL
async def get_context(db=Depends(get_db)):
    return {
        "db": db
    }

# Configurar el router de Strawberry
graphql_router = GraphQLRouter(schema, context_getter=get_context)

# Inicializar FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="Backend de catálogo de productos utilizando GraphQL, FastAPI y Arquitectura Limpia."
)

# Montar el endpoint de GraphQL
app.include_router(graphql_router, prefix="/graphql")

# Página de bienvenida HTML elegante
@app.get("/", response_class=HTMLResponse)
def root():
    html_content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Servidor GraphQL - Arquitectura Limpia</title>
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
        <style>
            :root {
                --primary: #9d4edd;
                --primary-dark: #7b2cbf;
                --primary-light: #c77dff;
                --bg: #0b090a;
                --surface: #161a1d;
                --surface-card: #202529;
                --text: #f8f9fa;
                --text-muted: #adb5bd;
                --success: #38b000;
            }
            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }
            body {
                font-family: 'Outfit', sans-serif;
                background-color: var(--bg);
                color: var(--text);
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                padding: 20px;
                overflow-x: hidden;
            }
            .background-glow {
                position: absolute;
                width: 600px;
                height: 600px;
                background: radial-gradient(circle, rgba(157, 78, 221, 0.15) 0%, rgba(0,0,0,0) 70%);
                top: -100px;
                left: -100px;
                z-index: -1;
                pointer-events: none;
            }
            .background-glow-right {
                position: absolute;
                width: 600px;
                height: 600px;
                background: radial-gradient(circle, rgba(199, 125, 255, 0.1) 0%, rgba(0,0,0,0) 70%);
                bottom: -100px;
                right: -100px;
                z-index: -1;
                pointer-events: none;
            }
            .card {
                background: rgba(22, 26, 29, 0.85);
                backdrop-filter: blur(16px);
                border: 1px solid rgba(157, 78, 221, 0.2);
                border-radius: 24px;
                padding: 40px;
                max-width: 800px;
                width: 100%;
                box-shadow: 0 20px 40px rgba(0,0,0,0.5);
                text-align: center;
                animation: fadeIn 0.8s ease-out;
            }
            h1 {
                font-size: 2.5rem;
                font-weight: 800;
                background: linear-gradient(135deg, var(--text) 30%, var(--primary-light) 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 15px;
            }
            .badge {
                display: inline-block;
                background: rgba(157, 78, 221, 0.15);
                border: 1px solid rgba(157, 78, 221, 0.4);
                color: var(--primary-light);
                padding: 6px 14px;
                border-radius: 50px;
                font-size: 0.85rem;
                font-weight: 600;
                margin-bottom: 25px;
            }
            p.description {
                color: var(--text-muted);
                font-size: 1.1rem;
                line-height: 1.6;
                margin-bottom: 30px;
            }
            .architecture-container {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 12px;
                margin-bottom: 35px;
                text-align: left;
            }
            .layer {
                background: var(--surface-card);
                border-radius: 12px;
                padding: 15px;
                border-left: 4px solid var(--primary);
                transition: transform 0.3s ease;
            }
            .layer:hover {
                transform: translateY(-5px);
            }
            .layer-title {
                font-weight: 600;
                font-size: 0.9rem;
                margin-bottom: 6px;
                color: var(--primary-light);
            }
            .layer-desc {
                font-size: 0.75rem;
                color: var(--text-muted);
            }
            .btn {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
                color: white;
                text-decoration: none;
                font-weight: 600;
                font-size: 1.1rem;
                padding: 16px 36px;
                border-radius: 50px;
                box-shadow: 0 10px 20px rgba(157, 78, 221, 0.3);
                transition: all 0.3s ease;
                border: none;
                cursor: pointer;
            }
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 15px 25px rgba(157, 78, 221, 0.5);
                background: linear-gradient(135deg, var(--primary-light) 0%, var(--primary) 100%);
            }
            .footer {
                margin-top: 30px;
                font-size: 0.8rem;
                color: rgba(248, 249, 250, 0.4);
            }
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
            @media (max-width: 600px) {
                .architecture-container {
                    grid-template-columns: 1fr;
                }
                .card {
                    padding: 25px;
                }
            }
        </style>
    </head>
    <body>
        <div class="background-glow"></div>
        <div class="background-glow-right"></div>
        <div class="card">
            <h1>Servicio API GraphQL Declarativo</h1>
            <span class="badge">FastAPI + Strawberry GraphQL + SQLAlchemy</span>
            <p class="description">
                Esta aplicación web implementa la consulta de productos de forma declarativa utilizando GraphQL. 
                Construida siguiendo los principios de la <strong>Arquitectura Limpia</strong>, dividida en capas desacopladas 
                para asegurar robustez, mantenibilidad y escalabilidad.
            </p>
            
            <div class="architecture-container">
                <div class="layer">
                    <div class="layer-title">Dominio</div>
                    <div class="layer-desc">Entidades puras de negocio y puertos (interfaces) abstractos.</div>
                </div>
                <div class="layer">
                    <div class="layer-title">Aplicación</div>
                    <div class="layer-desc">Casos de Uso del CRUD de productos agnósticos al framework.</div>
                </div>
                <div class="layer">
                    <div class="layer-title">Adaptadores</div>
                    <div class="layer-desc">Repositorio ORM (SQLAlchemy) y Resolvers GraphQL de Strawberry.</div>
                </div>
                <div class="layer">
                    <div class="layer-title">Infraestructura</div>
                    <div class="layer-desc">Conexión de BD SQLite y Servidor Web FastAPI.</div>
                </div>
            </div>
            
            <a href="/graphql" class="btn" target="_blank">Explorar GraphiQL Playground</a>
        </div>
        <div class="footer">
            Diseño e Implementación de Maestría en Ingeniería - gRPC & GraphQL Apps
        </div>
    </body>
    </html>
    """
    return html_content
