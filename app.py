from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from mysql.connector import Error
from functools import wraps
from config import DB_CONFIG

app = Flask(__name__)

# Clave secreta necesaria para usar sesiones (cámbiala por una más larga en un proyecto real)
app.secret_key = "clave_super_secreta_para_sesiones"

# Usuarios de la práctica (todos con la misma contraseña "1234")
USERS = {
    "abel": "1234",
    "amina": "1234",
    "rodrigo": "1234",
    "luciano": "1234",
    "thomas": "1234",
    "jeanpierre": "1234"
}


def get_db_connection():
    """Devuelve una conexión a la base de datos MySQL."""
    return mysql.connector.connect(**DB_CONFIG)


def login_required(f):
    """
    Decorador para proteger rutas.
    Si no hay usuario en sesión, redirige a /login.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


@app.route("/")
def index():
    """Página de inicio básica que muestra el número de presos."""
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


# -----------------------
# RUTAS DE AUTENTICACIÓN
# -----------------------

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Login sencillo:
    - GET: muestra formulario.
    - POST: verifica usuario y contraseña contra el diccionario USERS.
    """
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in USERS and USERS[username] == password:
            session["username"] = username
            return redirect(url_for("listar_presos"))
        else:
            error = "Usuario o contraseña incorrectos"

    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    """Cerrar sesión: elimina el usuario de la sesión y redirige a /login."""
    session.pop("username", None)
    return redirect(url_for("login"))


# -----------------------
# CRUD PRESO (PROTEGIDO)
# -----------------------

@app.route("/presos")
@login_required
def listar_presos():
    """Lista los presos con JOIN a PABELLON y DELITO."""
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
@login_required
def nuevo_preso():
    """Crea un nuevo preso."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

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
@login_required
def editar_preso(id_preso):
    """Edita un preso existente."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

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

    # GET: cargar datos del preso
    cursor.execute("SELECT * FROM PRESO WHERE id_preso = %s", (id_preso,))
    preso = cursor.fetchone()
    cursor.close()
    conn.close()

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
@login_required
def eliminar_preso(id_preso):
    """Elimina un preso de la base de datos."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM PRESO WHERE id_preso = %s", (id_preso,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("listar_presos"))


if __name__ == "__main__":
    app.run(debug=True)
