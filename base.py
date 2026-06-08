import psycopg2

# Crear base de datos
def inicializar_base_datos():
    db_params = {
        "host": "localhost",
        "user": "postgres",
        "password": "password",
        "port": "5432"
    }

    try:
        conexion = psycopg2.connect(**db_params)
        conexion.autocommit = True
        cursor = conexion.cursor()

        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'tp_distribuidos';")
        if not cursor.fetchone():
            cursor.execute("CREATE DATABASE tp_distribuidos;")
            print("Base de datos 'tp_distribuidos' creada con éxito.")

        cursor.close()
        conexion.close()

        # Conexión
        db_params["database"] = "tp_distribuidos"
        conexion_tp = psycopg2.connect(**db_params)
        cursor_tp = conexion_tp.cursor()

        # Crear la tabla con id y un campo de texto
        cursor_tp.execute("""
            CREATE TABLE IF NOT EXISTS tareas (
                id SERIAL PRIMARY KEY,
                texto TEXT NOT NULL
            );
        """)

        # Limpiar datos previos
        cursor_tp.execute("TRUNCATE TABLE tareas RESTART IDENTITY;")

        # registors de ejemplo
        registros_iniciales = [
            ("Procesar reporte de ventas mensual",),
            ("Optimizar índices de la base de datos",),
            ("Enviar notificaciones push pendientes",),
            ("Limpiar archivos temporales del sistema",)
        ]

        cursor_tp.executemany("INSERT INTO tareas (texto) VALUES (%s);", registros_iniciales)
        conexion_tp.commit()
        print("Tabla 'tareas' creada e inicializada con registros de prueba con éxito.")

    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
    finally:
        if 'conexion_tp' in locals() and conexion_tp:
            cursor_tp.close()
            conexion_tp.close()


if __name__ == "__main__":
    inicializar_base_datos()