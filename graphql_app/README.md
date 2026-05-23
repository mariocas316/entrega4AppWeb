# Catálogo de Productos - Servidor GraphQL (Clean Architecture)

Esta aplicación web implementa un servicio API GraphQL declarativo completo para la gestión de productos, utilizando **FastAPI**, **Strawberry GraphQL** y **SQLAlchemy** con **SQLite**.

El proyecto está estructurado bajo los principios de **Arquitectura Limpia (Clean Architecture)** para asegurar que las reglas de negocio estén aisladas de la base de datos y de la forma de entrega (web/protocolo).

---

## Arquitectura de Capas

El código está organizado de la siguiente manera:
1. **Dominio (`app/domain`)**: Contiene la entidad `Producto` y el puerto (interfaz abstracta) `ProductRepository`.
2. **Aplicación (`app/application`)**: Implementa los Casos de Uso del CRUD de productos de manera agnóstica a los frameworks.
3. **Adaptadores (`app/adapters`)**:
   * **database**: Implementación de base de datos con SQLAlchemy (`SQLAlchemyProductRepository`) mapeando a la tabla SQLite.
   * **graphql**: Definición de los esquemas, tipos y resolvers de Strawberry GraphQL.
4. **Infraestructura (`app/infrastructure`)**: Conexión de base de datos, configuración y montaje del servidor web FastAPI.

---

## Requisitos de Instalación

1. Asegúrate de tener Python 3.10+ instalado.
2. Crea un entorno virtual e instala las dependencias:
   ```bash
   python -m venv venv
   # En Windows:
   .\venv\Scripts\activate
   # En macOS/Linux:
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```

---

## Ejecución del Servidor

Para arrancar el servidor de desarrollo, ejecuta el siguiente comando desde el directorio `graphql_app`:
```bash
python -m app.main
```
El servidor se iniciará en `http://localhost:8000`.

---

## Pruebas con GraphiQL

Abre tu navegador y navega a:
[http://localhost:8000/graphql](http://localhost:8000/graphql)

Allí podrás ejecutar las siguientes operaciones declarativas de prueba:

### 1. Crear un Producto (Mutation)
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

### 2. Listar Todos los Productos (Query)
```graphql
query {
  obtenerProductos {
    id
    nombre
    precio
  }
}
```

### 3. Obtener un Producto por ID (Query)
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

### 4. Actualizar un Producto (Mutation)
```graphql
mutation {
  actualizarProducto(input: {
    id: 1,
    nombre: "Laptop Pro 16 Plus",
    precio: 1599.99
  }) {
    id
    nombre
    precio
  }
}
```

### 5. Eliminar un Producto (Mutation)
```graphql
mutation {
  eliminarProducto(id: 1)
}
```

### 6. Prueba de Manejo de Errores
Intenta crear un producto con precio negativo:
```graphql
mutation {
  crearProducto(input: {
    nombre: "Producto Erróneo",
    precio: -50.0
  }) {
    id
    nombre
  }
}
```
*Deberías ver un error controlado indicando que el precio no puede ser negativo.*
