# grpcApps: Guia rapida de ejecucion

Este repositorio contiene dos aplicaciones backend en Python:

- `graphql_app`: API GraphQL con FastAPI + Strawberry.
- `grpc_app`: Servidor gRPC + pasarela REST con FastAPI.

## 1) Requisitos

- Python 3.10 o superior
- PowerShell (Windows) o terminal equivalente

## 2) Crear y activar entorno virtual (una sola vez)

Desde la raiz del repositorio:

```bash
python -m venv venv
```

Activar entorno virtual:

```bash
# Windows (PowerShell)
.\venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

## 3) Instalar dependencias

Instala dependencias de cada app por separado:

```bash
# GraphQL
cd graphql_app
pip install -r requirements.txt
cd ..

# gRPC
cd grpc_app
pip install -r requirements.txt
cd ..
```

## 4) Ejecutar la app GraphQL

En una terminal ubicada en `graphql_app` (con el venv activo):

```bash
cd graphql_app
python -m app.main
```

Servidor disponible en:

- `http://localhost:8000`
- Playground GraphiQL: `http://localhost:8000/graphql`

Prueba automatizada de ejemplo (en otra terminal):

```bash
cd graphql_app
python test_graphql.py
```

## 5) Ejecutar la app gRPC + Gateway REST

En una terminal ubicada en `grpc_app` (con el venv activo):

```bash
cd grpc_app
python -m app.main
```

Servicios disponibles en:

- gRPC nativo: `localhost:50051`
- Gateway REST: `http://localhost:8001`
- Swagger del gateway: `http://localhost:8001/docs`
- Panel web: `http://localhost:8001`

Cliente de prueba gRPC (en otra terminal):

```bash
cd grpc_app
python client_test.py
```

## 6) (Opcional) Recompilar Protobuf

Solo si modificas `grpc_app/app/adapters/grpc/protos/product.proto`:

```bash
cd grpc_app
python compile_proto.py
```

## 7) Ejecutar ambas apps al mismo tiempo

Abre dos terminales con el entorno virtual activo:

- Terminal 1: `cd graphql_app` y `python -m app.main`
- Terminal 2: `cd grpc_app` y `python -m app.main`

## 8) Solucion rapida de problemas

- Si PowerShell bloquea scripts:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

- Si un puerto esta ocupado, cierra el proceso que lo usa o cambia la configuracion de puertos en cada aplicacion.
