from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


@app.route("/")
def index():
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
    try:
        conn = get_db_connection()
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
        return render_template("presos.html", presos=presos)
    except Error as e:
        return f"Error al obtener la lista de presos: {e}"


@app.route("/presos/nuevo", methods=["GET", "POST"])
def nuevo_preso():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Obtener datos para selects
    cursor.execute("SELECT id_pabellon, id_bloque, nombre FROM PABELLON ORDER BY id_pabellon;")
    pabellones = cursor.fetchall()

    cursor.execute("SELECT id_delito, nombre FROM DELITO ORDER BY id_delito;")
    delitos = cursor.fetchall()

    if request.method == "POST":
        nombre = request.form["nombre"]
        apellidos = request.form["apellidos"]
        dni = request.form["dni"]
        fecha_nacimiento = request.form["fecha_nacimiento"]
        fecha_ingreso = request.form["fecha_ingreso"]
        fecha_salida_prev = request.form["fecha_salida_prev"] or None
        id_pabellon = request.form["id_pabellon"]
        id_delito = request.form["id_delito"]
        observaciones = request.form["observaciones"] or None

        sql = """
            INSERT INTO PRESO
            (nombre, apellidos, dni, fecha_nacimiento, fecha_ingreso, fecha_salida_prev, 
             id_pabellon, id_delito, observaciones)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        valores = (
            nombre, apellidos, dni, fecha_nacimiento,
            fecha_ingreso, fecha_salida_prev, id_pabellon,
            id_delito, observaciones
        )
        cursor.execute(sql, valores)
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for("listar_presos"))

    # GET
    cursor.close()
    conn.close()
    return render_template(
        "preso_form.html",
        titulo_pagina="Nuevo preso",
        preso=None,
        pabellones=pabellones,
        delitos=delitos
    )


@app.route("/presos/editar/<int:id_preso>", methods=["GET", "POST"])
def editar_preso(id_preso):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Datos para selects
    cursor.execute("SELECT id_pabellon, id_bloque, nombre FROM PABELLON ORDER BY id_pabellon;")
    pabellones = cursor.fetchall()

    cursor.execute("SELECT id_delito, nombre FROM DELITO ORDER BY id_delito;")
    delitos = cursor.fetchall()

    if request.method == "POST":
        nombre = request.form["nombre"]
        apellidos = request.form["apellidos"]
        dni = request.form["dni"]
        fecha_nacimiento = request.form["fecha_nacimiento"]
        fecha_ingreso = request.form["fecha_ingreso"]
        fecha_salida_prev = request.form["fecha_salida_prev"] or None
        id_pabellon = request.form["id_pabellon"]
        id_delito = request.form["id_delito"]
        observaciones = request.form["observaciones"] or None

        sql = """
            UPDATE PRESO
            SET nombre = %s,
                apellidos = %s,
                dni = %s,
                fecha_nacimiento = %s,
                fecha_ingreso = %s,
                fecha_salida_prev = %s,
                id_pabellon = %s,
                id_delito = %s,
                observaciones = %s
            WHERE id_preso = %s
        """
        valores = (
            nombre, apellidos, dni, fecha_nacimiento,
            fecha_ingreso, fecha_salida_prev, id_pabellon,
            id_delito, observaciones, id_preso
        )
        cursor.execute(sql, valores)
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for("listar_presos"))

    # GET: obtener preso actual
    cursor.execute("SELECT * FROM PRESO WHERE id_preso = %s", (id_preso,))
    preso = cursor.fetchone()
    cursor.close()
    conn.close()

    # Adaptar fechas a string ISO YYYY-MM-DD (por si acaso)
    if preso:
        if preso["fecha_nacimiento"]:
            preso["fecha_nacimiento"] = preso["fecha_nacimiento"].isoformat()
        if preso["fecha_ingreso"]:
            preso["fecha_ingreso"] = preso["fecha_ingreso"].isoformat()
        if preso["fecha_salida_prev"]:
            preso["fecha_salida_prev"] = preso["fecha_salida_prev"].isoformat()

    return render_template(
        "preso_form.html",
        titulo_pagina="Editar preso",
        preso=preso,
        pabellones=pabellones,
        delitos=delitos
    )


@app.route("/presos/eliminar/<int:id_preso>", methods=["POST"])
def eliminar_preso(id_preso):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM PRESO WHERE id_preso = %s", (id_preso,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("listar_presos"))


if __name__ == "__main__":
    app.run(debug=True)
