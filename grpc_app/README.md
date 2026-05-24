# gRPC App - Guia de ejecucion

Servicio gRPC para gestion de productos con FastAPI como gateway REST.

## Requisitos

- Python 3.10 o superior
- Entorno virtual activo

Si estas en la raiz del repositorio, puedes activar el entorno asi:

```bash
# Windows (PowerShell)
.\venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

## Instalar dependencias

Desde esta carpeta (`grpc_app`):

```bash
pip install -r requirements.txt
```

## Ejecutar servidor gRPC + gateway

```bash
python -m app.main
```

Servicios disponibles:

- gRPC nativo: localhost:50051
- Gateway REST: http://localhost:8001
- Swagger: http://localhost:8001/docs
- Panel web: http://localhost:8001

## Ejecutar cliente de pruebas gRPC

En otra terminal (con el entorno virtual activo):

```bash
python client_test.py
```

## Recompilar Protobuf (opcional)

Si modificas `app/adapters/grpc/protos/product.proto`:

```bash
python compile_proto.py
```

Este script genera/actualiza archivos en `app/adapters/grpc/generated` y ajusta imports necesarios.

## Nota

Para una guia unificada de todo el repositorio (GraphQL + gRPC), revisa el README de la raiz.
