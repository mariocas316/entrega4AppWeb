# Catálogo de Productos - Servidor gRPC & Pasarela REST (Clean Architecture)

Esta aplicación web implementa un servicio **gRPC** nativo e intercambio de información punto a punto en tiempo real para la gestión de productos, utilizando **FastAPI**, **grpcio** y **SQLAlchemy** con **SQLite**.

El proyecto está estructurado bajo los principios de **Arquitectura Limpia (Clean Architecture)** para asegurar que las reglas de negocio estén aisladas del protocolo HTTP/2 (gRPC) y de la base de datos local.

Adicionalmente, se incluye una **Pasarela/Gateway REST** en FastAPI que traduce las llamadas del navegador a llamadas de alta velocidad gRPC nativas, sirviendo un Panel de Control visual e interactivo en HTML.

---

## Arquitectura de Capas

El código está organizado de la siguiente manera:
1. **Dominio (`app/domain`)**: Contiene la entidad `Producto` y el puerto (interfaz abstracta) `ProductRepository`.
2. **Aplicación (`app/application`)**: Implementa los Casos de Uso del CRUD de productos de manera agnóstica a los frameworks.
3. **Adaptadores (`app/adapters`)**:
   * **database**: Implementación de base de datos con SQLAlchemy (`SQLAlchemyProductRepository`) mapeando a la tabla SQLite.
   * **grpc**: Contrato de servicios Protobuf (`product.proto`), archivos auto-generados (`generated/`) y controladores gRPC (`controllers.py`) que traducen las peticiones RPC a casos de uso.
4. **Infraestructura (`app/infrastructure`)**: Servidor gRPC asíncrono, Gateway REST FastAPI con inyección de dependencias y página del Panel de Control en HTML5.

---

## Requisitos de Instalación

1. Asegúrate de tener Python 3.10+ instalado.
2. Crea un entorno virtual e instala las dependencias (se recomienda usar el entorno virtual compartido en la raíz del repositorio):
   ```bash
   python -m venv venv
   # En Windows:
   .\venv\Scripts\activate
   # En macOS/Linux:
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```

---

## Compilación de Protobuf (.proto)

Si modificas el archivo `app/adapters/grpc/protos/product.proto`, debes recompilar los archivos gRPC y Protobuf de Python ejecutando la siguiente línea desde la carpeta `grpc_app`:
```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. app/adapters/grpc/protos/product.proto
```
*(Nota: Para resolver las rutas de importación bajo Clean Architecture, hemos colocado los archivos compilados directamente en el directorio `app/adapters/grpc/generated/` modificando los paths generados. Los archivos ya se encuentran compilados de forma correcta).*

---

## Ejecución de los Servidores (gRPC + Gateway REST)

Ambos servidores (el servidor gRPC nativo en el puerto `50051` y el Gateway en el puerto `8001`) se inician en un único proceso asíncrono unificado ejecutando desde el directorio `grpc_app`:
```bash
python -m app.main
```

---

## Pruebas de Funcionamiento

Tienes **tres formas excelentes** de probar el CRUD completo del servidor gRPC:

### 1. Panel de Control Interactivo (Recomendado)
Abre tu navegador en:
[http://localhost:8001](http://localhost:8001)
Allí encontrarás un dashboard premium para Crear, Leer, Actualizar y Eliminar productos visualmente. Cada acción del dashboard realiza una llamada HTTP al Gateway REST, el cual hace un request **gRPC** nativo al servidor sobre el puerto `50051` y retorna la respuesta de inmediato.

### 2. Documentación Swagger UI
Abre tu navegador en:
[http://localhost:8001/docs](http://localhost:8001/docs)
Allí podrás probar todos los endpoints REST expuestos por la pasarela, los cuales se traducen internamente a llamadas gRPC.

### 3. Script de Pruebas de Consola (gRPC Puro)
Abre una terminal secundaria con el entorno virtual activo y ejecuta el cliente gRPC en Python puro:
```bash
python client_test.py
```
Este script realiza el ciclo CRUD completo directo al puerto `50051` mediante gRPC y muestra las respuestas de forma visual en la consola, incluyendo una demostración del manejo correcto de errores y códigos de estado gRPC (`StatusCode.NOT_FOUND` e `INVALID_ARGUMENT`).
