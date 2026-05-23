import grpc
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional, List

from app.infrastructure.config import settings
from app.adapters.grpc.generated import product_pb2
from app.adapters.grpc.generated import product_pb2_grpc

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="Pasarela REST (Gateway API) que traduce peticiones HTTP a llamadas de alta velocidad gRPC sobre HTTP/2."
)

# Modelos Pydantic para la documentación de Swagger de la Pasarela REST
class ProductoCrearSchema(BaseModel):
    nombre: str = Field(..., description="Nombre del producto")
    descripcion: Optional[str] = Field(None, description="Descripción del producto")
    precio: float = Field(..., description="Precio del producto, debe ser mayor o igual a cero")

class ProductoActualizarSchema(BaseModel):
    nombre: Optional[str] = Field(None, description="Nuevo nombre del producto")
    descripcion: Optional[str] = Field(None, description="Nueva descripción del producto")
    precio: Optional[float] = Field(None, description="Nuevo precio del producto")

class ProductoResponseSchema(BaseModel):
    id: int
    nombre: str
    descripcion: str
    precio: float

# Helper para canal gRPC asíncrono
def get_grpc_stub():
    channel = grpc.aio.insecure_channel(settings.GRPC_TARGET)
    stub = product_pb2_grpc.ProductServiceStub(channel)
    return channel, stub

def map_grpc_error(e: grpc.RpcError):
    """
    Traduce los códigos de error estándar de gRPC a excepciones HTTP de FastAPI.
    """
    code = e.code()
    details = e.details()
    if code == grpc.StatusCode.NOT_FOUND:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=details)
    elif code == grpc.StatusCode.INVALID_ARGUMENT:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=details)
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error en servidor gRPC: {details}")

# Endpoints REST expuestos por el Gateway
@app.post("/api/productos", response_model=ProductoResponseSchema, status_code=status.HTTP_201_CREATED)
async def crear_producto(payload: ProductoCrearSchema):
    channel, stub = get_grpc_stub()
    try:
        async with channel:
            # Enviamos el request Protobuf al servidor gRPC
            request = product_pb2.CreateProductRequest(
                nombre=payload.nombre,
                descripcion=payload.descripcion or "",
                precio=payload.precio
            )
            response = await stub.CreateProduct(request)
            return {
                "id": response.id,
                "nombre": response.nombre,
                "descripcion": response.descripcion,
                "precio": response.precio
            }
    except grpc.RpcError as e:
        map_grpc_error(e)

@app.get("/api/productos", response_model=List[ProductoResponseSchema])
async def listar_productos():
    channel, stub = get_grpc_stub()
    try:
        async with channel:
            request = product_pb2.EmptyRequest()
            response = await stub.ListProducts(request)
            return [
                {
                    "id": p.id,
                    "nombre": p.nombre,
                    "descripcion": p.descripcion,
                    "precio": p.precio
                }
                for p in response.productos
            ]
    except grpc.RpcError as e:
        map_grpc_error(e)

@app.get("/api/productos/{producto_id}", response_model=ProductoResponseSchema)
async def obtener_producto(producto_id: int):
    channel, stub = get_grpc_stub()
    try:
        async with channel:
            request = product_pb2.GetProductRequest(id=producto_id)
            response = await stub.GetProduct(request)
            return {
                "id": response.id,
                "nombre": response.nombre,
                "descripcion": response.descripcion,
                "precio": response.precio
            }
    except grpc.RpcError as e:
        map_grpc_error(e)

@app.put("/api/productos/{producto_id}", response_model=ProductoResponseSchema)
async def actualizar_producto(producto_id: int, payload: ProductoActualizarSchema):
    channel, stub = get_grpc_stub()
    try:
        async with channel:
            # Preparamos los opcionales en Protobuf
            kwargs = {"id": producto_id}
            if payload.nombre is not None:
                kwargs["nombre"] = payload.nombre
            if payload.descripcion is not None:
                kwargs["descripcion"] = payload.descripcion
            if payload.precio is not None:
                kwargs["precio"] = payload.precio

            request = product_pb2.UpdateProductRequest(**kwargs)
            response = await stub.UpdateProduct(request)
            return {
                "id": response.id,
                "nombre": response.nombre,
                "descripcion": response.descripcion,
                "precio": response.precio
            }
    except grpc.RpcError as e:
        map_grpc_error(e)

@app.delete("/api/productos/{producto_id}")
async def eliminar_producto(producto_id: int):
    channel, stub = get_grpc_stub()
    try:
        async with channel:
            request = product_pb2.DeleteProductRequest(id=producto_id)
            response = await stub.DeleteProduct(request)
            return {
                "success": response.success,
                "message": response.message
            }
    except grpc.RpcError as e:
        map_grpc_error(e)

# Interfaz Web Premium en la raíz del Gateway
@app.get("/", response_class=HTMLResponse)
def root():
    html_content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Panel de Control gRPC - Arquitectura Limpia</title>
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
        <style>
            :root {
                --primary: #00b4d8;
                --primary-dark: #0077b6;
                --primary-light: #90e0ef;
                --bg: #03045e;
                --surface: #023e8a;
                --card-bg: rgba(2, 62, 138, 0.45);
                --text: #caf0f8;
                --text-white: #ffffff;
                --text-muted: #90e0ef;
                --error: #ff4d4f;
                --success: #38b000;
            }
            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }
            body {
                font-family: 'Outfit', sans-serif;
                background: linear-gradient(135deg, #03045e 0%, #0077b6 100%);
                color: var(--text);
                min-height: 100vh;
                padding: 30px;
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            .container {
                max-width: 1100px;
                width: 100%;
                z-index: 1;
            }
            header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 40px;
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                padding: 20px 40px;
                border-radius: 20px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            }
            header h1 {
                font-size: 1.8rem;
                font-weight: 800;
                color: var(--text-white);
                background: linear-gradient(135deg, var(--text-white) 30%, var(--primary-light) 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            .badge-live {
                display: inline-flex;
                align-items: center;
                background: rgba(56, 176, 0, 0.15);
                border: 1px solid rgba(56, 176, 0, 0.4);
                color: #52b788;
                padding: 4px 12px;
                border-radius: 50px;
                font-size: 0.8rem;
                font-weight: 700;
            }
            .badge-live::before {
                content: '';
                display: inline-block;
                width: 8px;
                height: 8px;
                background-color: var(--success);
                border-radius: 50%;
                margin-right: 8px;
                animation: pulse 1.5s infinite;
            }
            .grid {
                display: grid;
                grid-template-columns: 1fr 2fr;
                gap: 30px;
            }
            .panel {
                background: var(--card-bg);
                backdrop-filter: blur(12px);
                border: 1px solid rgba(144, 224, 239, 0.2);
                border-radius: 24px;
                padding: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            .panel-title {
                font-size: 1.3rem;
                font-weight: 700;
                color: var(--text-white);
                margin-bottom: 20px;
                display: flex;
                align-items: center;
                gap: 10px;
                border-bottom: 1px solid rgba(144, 224, 239, 0.2);
                padding-bottom: 10px;
            }
            .form-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                font-size: 0.9rem;
                margin-bottom: 8px;
                color: var(--text-muted);
                font-weight: 500;
            }
            input, textarea {
                width: 100%;
                padding: 12px 16px;
                background: rgba(3, 4, 94, 0.5);
                border: 1px solid rgba(144, 224, 239, 0.3);
                border-radius: 12px;
                color: var(--text-white);
                font-family: inherit;
                font-size: 0.95rem;
                transition: all 0.3s;
            }
            input:focus, textarea:focus {
                outline: none;
                border-color: var(--primary);
                box-shadow: 0 0 10px rgba(0, 180, 216, 0.3);
            }
            .btn {
                width: 100%;
                background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
                color: var(--text-white);
                border: none;
                padding: 14px;
                border-radius: 12px;
                font-size: 1rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s;
                box-shadow: 0 4px 15px rgba(0, 180, 216, 0.2);
            }
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(0, 180, 216, 0.4);
                background: linear-gradient(135deg, var(--primary-light) 0%, var(--primary) 100%);
            }
            .btn.btn-secondary {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                color: var(--text-white);
                margin-top: 10px;
            }
            .btn.btn-secondary:hover {
                background: rgba(255, 255, 255, 0.2);
            }
            .product-list {
                display: flex;
                flex-direction: column;
                gap: 15px;
                max-height: 550px;
                overflow-y: auto;
                padding-right: 5px;
            }
            .product-card {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 16px;
                padding: 20px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                transition: all 0.3s;
            }
            .product-card:hover {
                background: rgba(255, 255, 255, 0.1);
                border-color: var(--primary);
                transform: translateX(5px);
            }
            .product-info h3 {
                color: var(--text-white);
                font-size: 1.15rem;
                margin-bottom: 5px;
            }
            .product-info p {
                font-size: 0.85rem;
                color: var(--text-muted);
                margin-bottom: 8px;
            }
            .product-price {
                display: inline-block;
                background: rgba(0, 180, 216, 0.15);
                border: 1px solid rgba(0, 180, 216, 0.3);
                color: var(--primary-light);
                padding: 4px 10px;
                border-radius: 8px;
                font-weight: 700;
                font-size: 0.9rem;
            }
            .product-actions {
                display: flex;
                gap: 10px;
            }
            .action-btn {
                background: none;
                border: none;
                cursor: pointer;
                padding: 8px;
                border-radius: 8px;
                transition: all 0.2s;
                color: var(--text-muted);
            }
            .action-btn.edit:hover {
                background: rgba(0, 180, 216, 0.2);
                color: var(--primary-light);
            }
            .action-btn.delete:hover {
                background: rgba(255, 77, 79, 0.2);
                color: var(--error);
            }
            .empty-state {
                text-align: center;
                padding: 40px;
                color: var(--text-muted);
                font-size: 0.95rem;
            }
            .notification {
                position: fixed;
                bottom: 20px;
                right: 20px;
                padding: 15px 25px;
                border-radius: 12px;
                background: rgba(3, 4, 94, 0.9);
                border-left: 5px solid var(--primary);
                box-shadow: 0 10px 25px rgba(0,0,0,0.5);
                color: var(--text-white);
                transform: translateY(100px);
                opacity: 0;
                transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                z-index: 100;
            }
            .notification.show {
                transform: translateY(0);
                opacity: 1;
            }
            .notification.success { border-left-color: var(--success); }
            .notification.error { border-left-color: var(--error); }
            
            .swagger-link {
                background: rgba(255, 255, 255, 0.1);
                color: var(--text-white);
                text-decoration: none;
                font-weight: 600;
                padding: 8px 16px;
                border-radius: 10px;
                border: 1px solid rgba(255, 255, 255, 0.2);
                font-size: 0.9rem;
                transition: all 0.3s;
            }
            .swagger-link:hover {
                background: var(--primary);
                border-color: var(--primary);
            }

            @keyframes pulse {
                0% { box-shadow: 0 0 0 0 rgba(56, 176, 0, 0.5); }
                70% { box-shadow: 0 0 0 10px rgba(56, 176, 0, 0); }
                100% { box-shadow: 0 0 0 0 rgba(56, 176, 0, 0); }
            }
            
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }

            @media (max-width: 900px) {
                .grid { grid-template-columns: 1fr; }
                header { flex-direction: column; gap: 15px; text-align: center; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <div>
                    <h1>Panel de Control gRPC</h1>
                    <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 3px;">
                        Pasarela REST-to-gRPC sobre Protocolo HTTP/2 en tiempo real
                    </p>
                </div>
                <div style="display: flex; align-items: center; gap: 15px;">
                    <a href="/docs" class="swagger-link" target="_blank">Documentación Swagger (REST)</a>
                    <span class="badge-live">gRPC Activo [Puerto 50051]</span>
                </div>
            </header>

            <div class="grid">
                <!-- Formulario de Producto -->
                <div class="panel">
                    <div class="panel-title" id="form-title">
                        Crear Nuevo Producto
                    </div>
                    <form id="product-form">
                        <input type="hidden" id="product-id">
                        <div class="form-group">
                            <label for="nombre">Nombre del Producto *</label>
                            <input type="text" id="nombre" placeholder="Ej. Laptop Gaming Asus" required>
                        </div>
                        <div class="form-group">
                            <label for="descripcion">Descripción</label>
                            <textarea id="descripcion" rows="3" placeholder="Breve detalle del producto..."></textarea>
                        </div>
                        <div class="form-group">
                            <label for="precio">Precio (USD) *</label>
                            <input type="number" step="0.01" id="precio" placeholder="0.00" required>
                        </div>
                        <button type="submit" class="btn" id="submit-btn">Guardar Producto en gRPC</button>
                        <button type="button" class="btn btn-secondary" id="cancel-btn" style="display: none;">
                            Cancelar Edición
                        </button>
                    </form>
                </div>

                <!-- Lista de Productos -->
                <div class="panel">
                    <div class="panel-title">
                        Productos Registrados (Consulta gRPC)
                    </div>
                    <div class="product-list" id="product-list">
                        <!-- Cargados dinámicamente -->
                        <div class="empty-state">Conectando con el servidor gRPC y cargando productos...</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Notificaciones -->
        <div class="notification" id="notification">
            Mensaje del sistema
        </div>

        <script>
            const API_URL = '/api/productos';
            const productForm = document.getElementById('product-form');
            const submitBtn = document.getElementById('submit-btn');
            const cancelBtn = document.getElementById('cancel-btn');
            const formTitle = document.getElementById('form-title');
            const productList = document.getElementById('product-list');
            const notification = document.getElementById('notification');

            let isEditing = false;

            // Mostrar notificación flotante
            function showNotify(message, type = 'success') {
                notification.textContent = message;
                notification.className = `notification ${type} show`;
                setTimeout(() => {
                    notification.classList.remove('show');
                }, 3000);
            }

            // Obtener todos los productos
            async function fetchProducts() {
                try {
                    const response = await fetch(API_URL);
                    if (!response.ok) throw new Error('Error al listar productos');
                    const products = await response.json();
                    
                    if (products.length === 0) {
                        productList.innerHTML = `
                            <div class="empty-state">
                                No hay productos registrados aún. <br>
                                ¡Agrega el primero desde el formulario de la izquierda!
                            </div>
                        `;
                        return;
                    }

                    productList.innerHTML = products.map(product => `
                        <div class="product-card" style="animation: fadeIn 0.4s ease-out;">
                            <div class="product-info">
                                <h3>${product.nombre}</h3>
                                <p>${product.descripcion || 'Sin descripción.'}</p>
                                <span class="product-price">$ ${product.precio.toFixed(2)}</span>
                                <span style="font-size: 0.75rem; color: #8ecae6; margin-left: 10px;">ID: ${product.id}</span>
                            </div>
                            <div class="product-actions">
                                <button class="action-btn edit" onclick="startEdit(${product.id}, '${product.nombre.replace(/'/g, "\\'")}', '${(product.descripcion || '').replace(/'/g, "\\'")}', ${product.precio})" title="Editar">
                                    <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7M18.5 2.5a2.121 2.121 0 113 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                                </button>
                                <button class="action-btn delete" onclick="deleteProduct(${product.id})" title="Eliminar">
                                    <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
                                </button>
                            </div>
                        </div>
                    `).join('');
                } catch (error) {
                    productList.innerHTML = `<div class="empty-state" style="color: var(--error);">Error al cargar productos del servidor gRPC.</div>`;
                    showNotify(error.message, 'error');
                }
            }

            // Enviar formulario (Crear o Actualizar)
            productForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const id = document.getElementById('product-id').value;
                const nombre = document.getElementById('nombre').value;
                const descripcion = document.getElementById('descripcion').value;
                const precio = parseFloat(document.getElementById('precio').value);

                const payload = { nombre, descripcion, precio };

                try {
                    let response;
                    if (isEditing) {
                        // Invocación a endpoint de actualización REST -> gRPC
                        response = await fetch(`${API_URL}/${id}`, {
                            method: 'PUT',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(payload)
                        });
                    } else {
                        // Invocación a endpoint de creación REST -> gRPC
                        response = await fetch(API_URL, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(payload)
                        });
                    }

                    const result = await response.json();
                    if (!response.ok) {
                        throw new Error(result.detail || 'Error al procesar la solicitud');
                    }

                    showNotify(isEditing ? 'Producto actualizado en gRPC correctamente' : 'Producto creado en gRPC correctamente');
                    resetForm();
                    fetchProducts();
                } catch (error) {
                    showNotify(error.message, 'error');
                }
            });

            // Preparar modo edición
            window.startEdit = function(id, nombre, descripcion, precio) {
                isEditing = true;
                formTitle.textContent = 'Editar Producto';
                submitBtn.textContent = 'Actualizar Producto en gRPC';
                cancelBtn.style.display = 'block';
                
                document.getElementById('product-id').value = id;
                document.getElementById('nombre').value = nombre;
                document.getElementById('descripcion').value = descripcion;
                document.getElementById('precio').value = precio;
                
                document.getElementById('nombre').focus();
            };

            // Cancelar edición
            cancelBtn.addEventListener('click', resetForm);

            function resetForm() {
                isEditing = false;
                formTitle.textContent = 'Crear Nuevo Producto';
                submitBtn.textContent = 'Guardar Producto en gRPC';
                cancelBtn.style.display = 'none';
                productForm.reset();
                document.getElementById('product-id').value = '';
            }

            // Eliminar producto
            window.deleteProduct = async function(id) {
                if (!confirm('¿Estás seguro de que deseas eliminar este producto a través de gRPC?')) return;
                
                try {
                    const response = await fetch(`${API_URL}/${id}`, {
                        method: 'DELETE'
                    });
                    const result = await response.json();
                    
                    if (!response.ok) {
                        throw new Error(result.detail || 'Error al eliminar');
                    }

                    showNotify('Producto eliminado en gRPC con éxito');
                    if (isEditing && document.getElementById('product-id').value == id) {
                        resetForm();
                    }
                    fetchProducts();
                } catch (error) {
                    showNotify(error.message, 'error');
                }
            };

            // Carga inicial
            fetchProducts();
        </script>
    </body>
    </html>
    """
    return html_content
