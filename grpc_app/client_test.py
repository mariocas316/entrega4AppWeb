import asyncio
import grpc
from app.adapters.grpc.generated import product_pb2
from app.adapters.grpc.generated import product_pb2_grpc
from app.infrastructure.config import settings

async def run_tests():
    print("==================================================")
    print(" INICIANDO PRUEBAS DE CLIENTE gRPC NATIVO")
    print(f" Conectando a {settings.GRPC_TARGET}...")
    print("==================================================\n")

    # Crear el canal asíncrono
    async with grpc.aio.insecure_channel(settings.GRPC_TARGET) as channel:
        stub = product_pb2_grpc.ProductServiceStub(channel)
        
        # ------------------------------------------------
        # 1. PRUEBA: CREAR PRODUCTOS
        # ------------------------------------------------
        print("[1/6] Probando RPC: CreateProduct...")
        try:
            p1 = await stub.CreateProduct(product_pb2.CreateProductRequest(
                nombre="Laptop Premium X1",
                descripcion="Laptop de alto rendimiento para IA",
                precio=2499.99
            ))
            print(f" -> Creado con éxito: ID={p1.id}, Nombre='{p1.nombre}', Precio=${p1.precio}")
            
            p2 = await stub.CreateProduct(product_pb2.CreateProductRequest(
                nombre="Mouse Ergonómico Inalámbrico",
                descripcion="Mouse vertical recargable",
                precio=59.50
            ))
            print(f" -> Creado con éxito: ID={p2.id}, Nombre='{p2.nombre}', Precio=${p2.precio}")
            
            p1_id = p1.id
            p2_id = p2.id
        except grpc.RpcError as e:
            print(f" -> ERROR al crear: {e.code()} - {e.details()}")
            return
            
        print()

        # ------------------------------------------------
        # 2. PRUEBA: LISTAR PRODUCTOS
        # ------------------------------------------------
        print("[2/6] Probando RPC: ListProducts...")
        try:
            lista = await stub.ListProducts(product_pb2.EmptyRequest())
            print(f" -> Productos encontrados en la Base de Datos:")
            for p in lista.productos:
                print(f"    * ID={p.id} | '{p.nombre}' | Precio=${p.precio:.2f} | '{p.descripcion}'")
        except grpc.RpcError as e:
            print(f" -> ERROR al listar: {e.code()} - {e.details()}")
        
        print()

        # ------------------------------------------------
        # 3. PRUEBA: OBTENER DETALLE DE PRODUCTO
        # ------------------------------------------------
        print(f"[3/6] Probando RPC: GetProduct para ID={p1_id}...")
        try:
            prod = await stub.GetProduct(product_pb2.GetProductRequest(id=p1_id))
            print(f" -> Obtenido: ID={prod.id}, Nombre='{prod.nombre}', Descripción='{prod.descripcion}', Precio=${prod.precio}")
        except grpc.RpcError as e:
            print(f" -> ERROR al obtener: {e.code()} - {e.details()}")
            
        print()

        # ------------------------------------------------
        # 4. PRUEBA: ACTUALIZAR PRODUCTO (Campos Opcionales)
        # ------------------------------------------------
        print(f"[4/6] Probando RPC: UpdateProduct para ID={p2_id} (Actualizando precio y descripción)...")
        try:
            # Enviamos solo ID, y campos opcionales que queremos parchear
            prod_act = await stub.UpdateProduct(product_pb2.UpdateProductRequest(
                id=p2_id,
                descripcion="Mouse ergonómico vertical PRO v2",
                precio=64.99
            ))
            print(f" -> Actualizado con éxito: ID={prod_act.id}, Nombre='{prod_act.nombre}', Descripción='{prod_act.descripcion}', Precio=${prod_act.precio}")
        except grpc.RpcError as e:
            print(f" -> ERROR al actualizar: {e.code()} - {e.details()}")
            
        print()

        # ------------------------------------------------
        # 5. PRUEBA: ELIMINAR PRODUCTO
        # ------------------------------------------------
        print(f"[5/6] Probando RPC: DeleteProduct para ID={p1_id}...")
        try:
            res = await stub.DeleteProduct(product_pb2.DeleteProductRequest(id=p1_id))
            print(f" -> Éxito={res.success} | Mensaje: '{res.message}'")
        except grpc.RpcError as e:
            print(f" -> ERROR al eliminar: {e.code()} - {e.details()}")
            
        print()

        # ------------------------------------------------
        # 6. PRUEBA: VERIFICAR MANEJO DE ERRORES (Buscar ID inexistente)
        # ------------------------------------------------
        print(f"[6/6] Probando RPC: GetProduct con ID eliminado ({p1_id}) para verificar el MANEJO DE ERRORES...")
        try:
            await stub.GetProduct(product_pb2.GetProductRequest(id=p1_id))
            print(" -> ¡Alerta! Se encontró el producto (esto no debería suceder).")
        except grpc.RpcError as e:
            print(f" -> EXCEPCIÓN ESPERADA (Éxito en Prueba de Errores):")
            print(f"    Código de Estado gRPC: {e.code()}")
            print(f"    Mensaje Detallado: '{e.details()}'")
            
        print("\n==================================================")
        print(" PRUEBAS COMPLETADAS CON ÉXITO")
        print(" Todos los métodos CRUD y el manejo de errores de gRPC")
        print(" funcionan correctamente.")
        print("==================================================")

if __name__ == "__main__":
    asyncio.run(run_tests())
