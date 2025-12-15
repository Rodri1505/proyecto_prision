from faker import Faker
import mysql.connector
from config import DB_CONFIG
import random

fake = Faker('es_ES')

# Cantidad de presos a generar
NUM_PRESOS = 20

con = mysql.connector.connect(**DB_CONFIG)
cursor = con.cursor()

for _ in range(NUM_PRESOS):

    nombre = fake.first_name()
    apellidos = fake.last_name() + " " + fake.last_name()
    dni = fake.unique.bothify(text="########?")  # ejemplo: 12345678A
    fecha_nacimiento = fake.date_of_birth(minimum_age=18, maximum_age=70)
    fecha_ingreso = fake.date_between(start_date='-10y', end_date='today')
    fecha_salida_prev = fake.date_between(start_date='today', end_date='+10y')
    id_pabellon = random.randint(1, 5)  # según tus inserts
    id_delito = random.randint(1, 5)   # según tus inserts
    observaciones = fake.sentence()

    sql = """
        INSERT INTO PRESO 
        (nombre, apellidos, dni, fecha_nacimiento, fecha_ingreso, fecha_salida_prev, 
         id_pabellon, id_delito, observaciones)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    valores = (
        nombre, apellidos, dni, fecha_nacimiento, fecha_ingreso,
        fecha_salida_prev, id_pabellon, id_delito, observaciones
    )

    cursor.execute(sql, valores)

con.commit()
cursor.close()
con.close()

print(f"{NUM_PRESOS} presos generados correctamente.")
