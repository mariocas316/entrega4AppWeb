import urllib.request
import json

GRAPHQL_URL = "http://localhost:8000/graphql"

def send_query(query: str, variables: dict = None) -> dict:
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
        
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        GRAPHQL_URL,
        data=data,
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req) as res:
            return json.loads(res.read().decode("utf-8"))
    except Exception as e:
        print(f"Error de red: {e}")
        return {}

def test_graphql():
    print("==================================================")
    print(" INICIANDO PRUEBAS DE CLIENTE GRAPHQL NATIVO")
    print(f" Enviando consultas a {GRAPHQL_URL}...")
    print("==================================================\n")

    # 1. PRUEBA: CREAR PRODUCTO
    print("[1/5] Enviando Mutation: crearProducto...")
    mutation_create = """
    mutation {
      crearProducto(input: {
        nombre: "Teclado Mecánico Inalámbrico",
        descripcion: "Teclado 60% con switches brown",
        precio: 89.99
      }) {
        id
        nombre
        descripcion
        precio
      }
    }
    """
    res = send_query(mutation_create)
    print("Respuesta recibida:")
    print(json.dumps(res, indent=4, ensure_ascii=False))
    
    if "errors" in res:
        print("ERROR al crear.")
        return
        
    p_id = res["data"]["crearProducto"]["id"]
    print()

    # 2. PRUEBA: LISTAR PRODUCTOS
    print("[2/5] Enviando Query: obtenerProductos...")
    query_list = """
    query {
      obtenerProductos {
        id
        nombre
        precio
      }
    }
    """
    res = send_query(query_list)
    print("Respuesta recibida:")
    print(json.dumps(res, indent=4, ensure_ascii=False))
    print()

    # 3. PRUEBA: ACTUALIZAR PRODUCTO
    print(f"[3/5] Enviando Mutation: actualizarProducto para ID={p_id}...")
    mutation_update = f"""
    mutation {{
      actualizarProducto(input: {{
        id: {p_id},
        nombre: "Teclado Mecánico RGB Pro",
        precio: 99.99
      }}) {{
        id
        nombre
        precio
      }}
    }}
    """
    res = send_query(mutation_update)
    print("Respuesta recibida:")
    print(json.dumps(res, indent=4, ensure_ascii=False))
    print()

    # 4. PRUEBA: MANEJO DE ERRORES (Precio Negativo)
    print("[4/5] Probando Validación: Crear producto con precio negativo...")
    mutation_error = """
    mutation {
      crearProducto(input: {
        nombre: "Mouse Barato",
        precio: -10.0
      }) {
        id
        nombre
      }
    }
    """
    res = send_query(mutation_error)
    print("Respuesta recibida (Se espera sección 'errors'):")
    print(json.dumps(res, indent=4, ensure_ascii=False))
    print()

    # 5. PRUEBA: ELIMINAR PRODUCTO
    print(f"[5/5] Enviando Mutation: eliminarProducto para ID={p_id}...")
    mutation_delete = f"""
    mutation {{
      eliminarProducto(id: {p_id})
    }}
    """
    res = send_query(mutation_delete)
    print("Respuesta recibida:")
    print(json.dumps(res, indent=4, ensure_ascii=False))
    print()

    print("==================================================")
    print(" PRUEBAS GRAPHQL COMPLETADAS CON ÉXITO")
    print("==================================================")

if __name__ == "__main__":
    test_graphql()
