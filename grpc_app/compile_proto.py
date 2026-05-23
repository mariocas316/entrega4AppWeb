import os
import subprocess
import sys

def compile_proto():
    print("==================================================")
    print(" COMPILADOR AUTOMÁTICO DE ARCHIVOS PROTO (gRPC)")
    print("==================================================")
    
    # Nos aseguramos de estar en el directorio correcto
    current_dir = os.path.basename(os.getcwd())
    if current_dir == "grpcApps":
        # Si estamos en la raíz, nos movemos a la subcarpeta grpc_app para ejecutar
        os.chdir("grpc_app")
        
    # Creamos el directorio de archivos generados si no existe
    generated_dir = "app/adapters/grpc/generated"
    os.makedirs(generated_dir, exist_ok=True)
    
    # Ejecutamos protoc usando el intérprete de Python actual (el del venv)
    cmd = [
        sys.executable,
        "-m", "grpc_tools.protoc",
        "-Iapp/adapters/grpc/protos",
        "--python_out=app/adapters/grpc/generated",
        "--grpc_python_out=app/adapters/grpc/generated",
        "app/adapters/grpc/protos/product.proto"
    ]
    
    print(f"Ejecutando comando: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print("\n[ERROR] Ocurrió un error al compilar el archivo proto:")
        print(result.stderr)
        sys.exit(1)
        
    print("\n[OK] Compilación exitosa de Protobuf y gRPC.")
    print("Ajustando importaciones relativas para Arquitectura Limpia...")
    
    # Reparar importación en product_pb2_grpc.py
    grpc_file_path = "app/adapters/grpc/generated/product_pb2_grpc.py"
    if os.path.exists(grpc_file_path):
        with open(grpc_file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        old_import = "import product_pb2 as product__pb2"
        new_import = "from app.adapters.grpc.generated import product_pb2 as product__pb2"
        
        if old_import in content:
            content = content.replace(old_import, new_import)
            with open(grpc_file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"[OK] Importación parchada con éxito en: {grpc_file_path}")
        else:
            print("[INFO] La importación ya estaba parchada o no requería modificación.")
            
    print("==================================================")
    print(" COMPILACIÓN COMPLETADA EXITOSAMENTE")
    print("==================================================")

if __name__ == "__main__":
    compile_proto()
