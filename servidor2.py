import socket
import threading
import psycopg2


def consultar_base_datos(id_tarea):
    try:
        conexion = psycopg2.connect(
            host="localhost",
            database="tp_distribuidos",
            user="postgres",
            password="password",
            port="5432"
        )
        cursor = conexion.cursor()
        cursor.execute("SELECT texto FROM tareas WHERE id = %s;", (id_tarea,))
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()

        if resultado:
            return resultado[0]
        return "Registro no encontrado"
    except Exception as e:
        return f"Error de conexión a DB: {e}"


def procesar_peticion(conexion, direccion):
    try:
        datos = conexion.recv(1024).decode('utf-8')
        if datos:
            print(f"[Worker 2] Consulta recibida para ID: {datos} desde {direccion}")
            texto_recuperado = consultar_base_datos(datos)

            respuesta = f"[Respuesta de Worker 2] ID {datos}: {texto_recuperado}"
            conexion.sendall(respuesta.encode('utf-8'))
    except Exception as e:
        print(f"[Worker 2] Error: {e}")
    finally:
        conexion.close()


def iniciar_servidor():
    host = 'localhost'
    puerto = 5002
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((host, puerto))
    servidor.listen(5)
    print(f"Servidor 2 (Worker) activo en puerto {puerto}...")

    try:
        while True:
            conexion, direccion = servidor.accept()
            hilo = threading.Thread(target=procesar_peticion, args=(conexion, direccion))
            hilo.start()
    except KeyboardInterrupt:
        print("\nApagando Servidor 2.")
    finally:
        servidor.close()


if __name__ == "__main__":
    iniciar_servidor()