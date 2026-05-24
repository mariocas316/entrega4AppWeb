# GraphQL App - Guia de ejecucion

Servicio API GraphQL para gestion de productos con FastAPI, Strawberry y SQLite.

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

Desde esta carpeta (`graphql_app`):

```bash
pip install -r requirements.txt
```

## Ejecutar servidor

```bash
python -m app.main
```

Servidor y playground:

- API base: http://localhost:8000
- GraphiQL: http://localhost:8000/graphql

## Ejecutar prueba automatizada

En otra terminal (con el entorno virtual activo):

```bash
python test_graphql.py
```

## Operaciones de prueba en GraphiQL

### Crear producto

```graphql
mutation {
  crearProducto(input: {
    nombre: "Laptop Pro 16",
    descripcion: "Laptop potente para desarrollo de software",
    precio: 1499.99
  }) {
    id
    nombre
    descripcion
    precio
  }
}
```

### Listar productos

```graphql
query {
  obtenerProductos {
    id
    nombre
    precio
  }
}
```

### Obtener producto por ID

```graphql
query {
  obtenerProducto(id: 1) {
    id
    nombre
    descripcion
    precio
  }
}
```

### Actualizar producto

```graphql
mutation {
  actualizarProducto(input: {
    id: 1,
    nombre: "Laptop Pro 16 Gen2",
    precio: 1599.99
  }) {
    id
    nombre
    precio
  }
}
```

### Eliminar producto

```graphql
mutation {
  eliminarProducto(id: 1)
}
```

## Nota

Para una guia unificada de todo el repositorio (GraphQL + gRPC), revisa el README de la raiz.
