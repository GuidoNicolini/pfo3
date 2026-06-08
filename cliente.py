import socket
import time


def consultar_registro(id_a_consultar):
    host = 'localhost'
    puerto = 5000  # Siempre se conecta al puerto del balanceador

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, puerto))
            print(f"Cliente -> Solicitando datos del ID: {id_a_consultar}")
            s.sendall(str(id_a_consultar).encode('utf-8'))

            respuesta = s.recv(1024).decode('utf-8')
            print(f"Cliente <- {respuesta}\n")
    except Exception as e:
        print(f"Error al conectar con el balanceador: {e}")


if __name__ == "__main__":
    ids_de_prueba = [1, 2, 3, 4]

    for id_test in ids_de_prueba:
        consultar_registro(id_test)
        time.sleep(1)