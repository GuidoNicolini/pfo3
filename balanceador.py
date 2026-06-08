import socket
import threading

SERVIDORES_WORKERS = [('localhost', 5001), ('localhost', 5002)]
turno = 0
lock = threading.Lock()


def manejar_cliente(conexion_cliente):
    global turno

    with lock:
        servidor_destino = SERVIDORES_WORKERS[turno]
        turno = (turno + 1) % len(SERVIDORES_WORKERS)

    try:
        backend = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        backend.connect(servidor_destino)

        # Recibir el ID solicitado por el cliente y mandarlo al worker
        id_solicitado = conexion_cliente.recv(1024)
        backend.sendall(id_solicitado)

        # Recibir la respuesta del worker (con el texto de la DB) y enviarla al cliente
        respuesta_worker = backend.recv(1024)
        conexion_cliente.sendall(respuesta_worker)

    except Exception as e:
        print(f"Error al conectar con el worker {servidor_destino}: {e}")
        conexion_cliente.sendall(b"Error: Worker no disponible.")
    finally:
        backend.close()
        conexion_cliente.close()


def iniciar_balanceador():
    host = 'localhost'
    puerto = 5000
    balanceador = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    balanceador.bind((host, puerto))
    balanceador.listen(5)
    print(f"Balanceador escuchando en {host}:{puerto}...")

    try:
        while True:
            conexion_cliente, _ = balanceador.accept()
            hilo = threading.Thread(target=manejar_cliente, args=(conexion_cliente,))
            hilo.start()
    except KeyboardInterrupt:
        print("Apagando balanceador.")
    finally:
        balanceador.close()


if __name__ == "__main__":
    iniciar_balanceador()