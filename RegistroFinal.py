import tkinter as tk
import sqlite3
from PIL import Image, ImageTk
from cv2 import aruco
import cv2
import cv2.aruco as aruco
import numpy as np

conn = sqlite3.connect('data.db')
cursor = conn.cursor()
cursor.execute('DROP TABLE IF EXISTS registros')
conn.commit()
conn.close()

conn = sqlite3.connect('data.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS registros (
        aruco INTEGER PRIMARY KEY,
        nombre TEXT,
        texto_prueba TEXT
    )
''')
conn.commit()
conn.close()

def generar_imagen_aruco(aruco_number):
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
    marker_img = aruco.generateImageMarker(aruco_dict, aruco_number, 200)
    return ImageTk.PhotoImage(image=Image.fromarray(marker_img))

def registrar_datos():
    nombre = entry_nombre.get()
    texto_prueba = entry_texto_prueba.get()

    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        cursor.execute('SELECT MAX("aruco") FROM "registros"')

        result = cursor.fetchone()[0]
        try:
            last_aruco = int(result) if result is not None else -1
        except (ValueError, TypeError):
            last_aruco = -1

        conn.close()

        new_aruco = last_aruco + 1

        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO "registros" ("aruco", "nombre", "texto_prueba") VALUES (?, ?, ?)
        ''', (new_aruco, nombre, texto_prueba))
        conn.commit()
        conn.close()

        image_aruco = generar_imagen_aruco(new_aruco)
        label_imagen_aruco.config(image=image_aruco)
        label_imagen_aruco.image = image_aruco

        label_resultado.config(text=f'Registro exitoso. Nuevo ArUco: {new_aruco}')

    except Exception as e:
        print(f"Error: {e}")



app_registro = tk.Tk()
app_registro.title("Registrar Datos")

label_nombre = tk.Label(app_registro, text="Nombre:")
label_nombre.pack()

entry_nombre = tk.Entry(app_registro)
entry_nombre.pack()

label_texto_prueba = tk.Label(app_registro, text="Texto de Prueba:")
label_texto_prueba.pack()

entry_texto_prueba = tk.Entry(app_registro)
entry_texto_prueba.pack()

button_registrar = tk.Button(app_registro, text="Registrar", command=registrar_datos)
button_registrar.pack()

label_resultado = tk.Label(app_registro, text='')
label_resultado.pack()

# Label to display the image of the ArUco
label_imagen_aruco = tk.Label(app_registro)
label_imagen_aruco.pack()

app_registro.mainloop()
