import mysql.connector

localhost_sesion = ""
user_sesion = ""
password_sesion = ""
database_sesion = ""

def conectar():
    return mysql.connector.connect(
        host=localhost_sesion,
        user=user_sesion,
        password=password_sesion,
        database=database_sesion
    )