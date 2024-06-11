import mysql.connector
import pandas as pd
from mysql.connector import Error
import webscrappy as wb

# esta funcion lo reutilize con el que use en el examen para conectarme ala base de datos
def conexion():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password='password',
            database='Pokemon'
        )
        if conexion.is_connected():
            print('Conexión exitosa')
            return conexion
    except Error as ex:
        print('Error durante la conexión', ex)
        return None


def importarDatosRegion(conexion, TablaRegion):
    cursor = conexion.cursor()
    df = TablaRegion.dropna()
    for _, row in df.iterrows():
        sql = """INSERT INTO region (Nombre) VALUES (%s)"""
        data = (row['Nombre'],)
        cursor.execute(sql, data)

    conexion.commit()
    cursor.close()
    print('Datos de región insertados super bien')


def importarDatosPokedex(conexion, TablaPokedex):
    cursor = conexion.cursor()
    df = TablaPokedex.dropna()
    for _, row in df.iterrows():
        sql = """INSERT INTO pokedex (Numero_de_pokedex, Numero_de_pokemonn) VALUES (%s, %s)"""
        data = (row['Numero de Pokedex'], row['Nombre de pokemon'])
        cursor.execute(sql, data)

    conexion.commit()
    cursor.close()
    print('Pokedex registrado con exito entrenador')


def importarDatosTipos(conexion, TablaTipos):
    cursor = conexion.cursor()
    df = TablaTipos.dropna()
    for _, row in df.iterrows():
        sql = """INSERT INTO tipos (Nombre) VALUES (%s)"""
        data = (row['Nombre'],)
        cursor.execute(sql, data)

    conexion.commit()
    cursor.close()
    print('Todos los tipos insertados con exito')



