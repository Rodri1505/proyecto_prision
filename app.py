# app.py
# Aplicación Flask para el sistema de gestión de prisión.

from flask import Flask, render_template
import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

app = Flask(__name__)


def get_db_connection():
    """
    Crea y devuelve una conexión a la base de datos MySQL
    utilizando los datos definidos en DB_CONFIG (config.py).
    """
    connection = mysql.connector.connect(**DB_CONFIG)
    return connection


@app.route("/")
def index():
    """
    Ruta principal.
    Solo muestra un mensaje de estado básico.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM PRESO;")
        num_presos = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        return f"Sistema de Gestión de Prisión OK. Número de presos en la BD: {num_presos}"

    except Error as e:
        return f"Error al conectar con la base de datos: {e}"


@app.route("/presos")
def listar_presos():
    """
    Ruta para listar los presos en una página HTML.
    - Recupera datos de PRESO + PABELLON + DELITO.
    - Envía la lista de presos a la plantilla 'presos.html'.
    """
    try:
        conn = get_db_connection()
        # dictionary=True hace que cada fila sea un diccionario {columna: valor}
        cursor = conn.cursor(dictionary=True)

        consulta = """
            SELECT 
                p.id_preso,
                p.nombre,
                p.apellidos,
                p.dni,
                p.fecha_ingreso,
                pb.nombre AS pabellon,
                d.nombre AS delito
            FROM PRESO p
            JOIN PABELLON pb ON p.id_pabellon = pb.id_pabellon
            JOIN DELITO d ON p.id_delito = d.id_delito
            ORDER BY p.id_preso;
        """

        cursor.execute(consulta)
        presos = cursor.fetchall()

        cursor.close()
        conn.close()

        # Enviamos la lista 'presos' a la plantilla presos.html
        return render_template("presos.html", presos=presos)

    except Error as e:
        return f"Error al obtener la lista de presos: {e}"


if __name__ == "__main__":
    app.run(debug=True)
