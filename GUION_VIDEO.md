# Guion Sugerido para el Video Explicativo (Máx. 15 Minutos)

Este guion te servirá de guía paso a paso para narrar y grabar tu video explicativo de la actividad de Maestría de forma profesional y fluida, asegurando cubrir todos los puntos clave evaluados en la rúbrica para obtener el puntaje máximo (**250/250**).

---

## Estructura del Video (Tiempos Sugeridos)

### 1. Introducción y Arquitectura (0:00 - 3:00)
* **Qué mostrar en pantalla**: Abre tu editor de código (VS Code o similar) y muestra la estructura general de carpetas de ambos proyectos (`graphql_app` y `grpc_app`).
* **Qué decir/narrar**:
  > *"Buenas tardes, mi nombre es [Tu Nombre]. En esta presentación voy a explicar el desarrollo de dos servicios backend construidos bajo el framework **FastAPI** en Python, implementando dos modelos modernos de API: **GraphQL** y **gRPC**. Ambos proyectos han sido diseñados bajo los principios estrictos de **Arquitectura Limpia (Clean Architecture)** para asegurar el desacoplamiento total de la lógica de negocio frente a la infraestructura técnica..."*
* **Explica las Capas en pantalla**:
  * **Dominio (`domain/`)**: Muestra `app/domain/entities.py`. Explica que `Producto` es una `dataclass` pura de Python, sin dependencias de base de datos ni frameworks, garantizando que las reglas de negocio (como validar que el precio no sea negativo) estén en el núcleo. Muestra también `repositories.py` indicando que es la interfaz abstracta (puerto).
  * **Aplicación (`application/`)**: Muestra `app/application/use_cases.py`. Señala que aquí residen los Casos de Uso del CRUD de productos de forma agnóstica.
  * **Adaptadores (`adapters/`)**: Explica que comunica el mundo exterior con la aplicación. Muestra `adapters/database` y el mapeo bidireccional entre la entidad de dominio y `ProductoDB` de SQLAlchemy, y muestra los resolvers de GraphQL o controladores gRPC.
  * **Infraestructura (`infrastructure/`)**: Muestra las conexiones a las bases de datos SQLite independientes y las configuraciones de los servidores FastAPI y gRPC.

---

### 2. Demostración y Pruebas del Proyecto 1: GraphQL (3:00 - 7:00)
* **Qué mostrar en pantalla**: Abre una terminal en tu editor y muestra que el servidor de GraphQL está corriendo en `http://localhost:8000` (`python -m app.main`). Luego, abre tu navegador web en [http://localhost:8000/graphql](http://localhost:8000/graphql) para abrir el playground **GraphiQL**.
* **Qué decir/narrar**:
  > *"Aquí vemos el servidor GraphQL corriendo con FastAPI y Strawberry. Al ingresar al playground de GraphiQL en el puerto 8000, podemos ejecutar consultas declarativas. GraphQL nos permite solicitar únicamente la información que necesitamos, evitando el sub-consultado o sobre-consultado (underfetching o overfetching) típico de REST..."*
* **Acciones en vivo a realizar**:
  1. **Crear Producto**: Copia y ejecuta la mutation `crearProducto` (del README) para registrar un producto (ej. *"Teclado Mecánico"* por $89.99). Muestra que se guarda y retorna su ID.
  2. **Listar Productos**: Ejecuta la query `obtenerProductos` solicitando solo el `id` y `precio`. Explica que esto ilustra la consulta declarativa y eficiente de información.
  3. **Actualizar Producto**: Ejecuta la mutation `actualizarProducto` modificando el precio a $99.99.
  4. **Probar Manejo de Errores**: Intenta crear un producto con precio negativo (ej. -$20.0). Ejecútalo y muestra cómo el resolver atrapa la excepción y retorna un error JSON limpio y descriptivo en la sección `errors`: *"El precio del producto no puede ser negativo"*.
  5. **Eliminar Producto**: Ejecuta la mutation `eliminarProducto` para demostrar el CRUD completo.

---

### 3. Demostración y Pruebas del Proyecto 2: gRPC (7:00 - 12:00)
* **Qué mostrar en pantalla**: Abre la carpeta `grpc_app`. Muestra la terminal con el servidor unificado corriendo en el puerto 8001 para la Pasarela y en el 50051 para gRPC (`python -m app.main`).
* **Qué decir/narrar**:
  > *"A continuación, revisamos el proyecto de gRPC. gRPC utiliza HTTP/2 para comunicación punto a punto de alto rendimiento en tiempo real y serializa los datos con Protocol Buffers. Aquí vemos el archivo product.proto con la definición del contrato de servicio. Hemos configurado un servidor gRPC nativo asíncrono sobre el puerto 50051, y una Pasarela REST en FastAPI en el puerto 8001 que traduce peticiones REST a gRPC para pruebas web rápidas..."*
* **Acciones en vivo a realizar**:
  1. **Prueba en Consola (gRPC Puro)**: Abre otra terminal, activa el entorno virtual y ejecuta:
     ```bash
     python client_test.py
     ```
     Muestra en vivo cómo se conecta al puerto `50051`, realiza la creación, consulta, actualización y eliminación de forma ultra veloz, mostrando además la excepción controlada `StatusCode.NOT_FOUND` al buscar un ID eliminado. Explica que esto comprueba que el servidor gRPC nativo funciona de forma sobresaliente.
  2. **Prueba en el Navegador (Gateway y Dashboard)**: Abre tu navegador en [http://localhost:8001](http://localhost:8001). Muestra el **Panel de Control** de gRPC en HTML.
     * Agrega un nuevo producto usando el formulario. Muestra cómo aparece instantáneamente en la lista de la derecha.
     * Edita el producto (cambiando precio o descripción) y observa cómo se actualiza.
     * Elimina el producto y comprueba que desaparece.
     * Abre [http://localhost:8001/docs](http://localhost:8001/docs) para mostrar la documentación interactiva de Swagger UI de la pasarela.

---

### 4. Repositorio de GitHub y Conclusión (12:00 - 15:00)
* **Qué mostrar en pantalla**: Abre el archivo `.gitignore` y explica la limpieza del proyecto. Si ya subiste el código, puedes abrir tu perfil de GitHub y mostrar el repositorio con el código fuente estructurado e impecable.
* **Qué decir/narrar**:
  > *"Para cumplir rigurosamente con la rúbrica de entrega, el repositorio de GitHub se encuentra estructurado con ambos proyectos organizados de forma independiente. Contamos con un archivo .gitignore global que excluye de forma automática cachés, entornos virtuales y bases de datos locales, garantizando que el repositorio esté sumamente limpio y ordenado sin archivos innecesarios. Ambos proyectos contienen un archivo README.md instructivo con la guía de instalación y ejecución..."*
  >
  > *"Como conclusión, esta práctica nos permite contrastar el enfoque declarativo de GraphQL frente a la comunicación en tiempo real y de alto rendimiento que nos ofrece gRPC a través de HTTP/2 y Protocol Buffers. Ambos enfoques resuelven los desafíos del REST tradicional en diferentes escenarios empresariales..."*
* **Cierre**: Despídete amablemente.

---

¡Mucho éxito con tu grabación! Siguiendo esta guía paso a paso, tu video tendrá una estructura académica y técnica de altísimo nivel.
