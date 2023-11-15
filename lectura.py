import tkinter as tk
import cv2
from tkinter import PhotoImage
import sqlite3
from PIL import Image, ImageTk

def obtener_datos(apriltag):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM registros WHERE apriltag = ?', (apriltag,))
    data = cursor.fetchone()
    conn.close()

    if data:
        resultado = f"Nombre: {data[2]}\nTexto de Prueba: {data[3]}"
    else:
        resultado = "Apriltag no encontrado"

    label_resultado.config(text=resultado)

# Función para actualizar la imagen de la cámara
def actualizar_camara():
    ret, frame = cap.read()
    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detectar AprilTag
        apriltags = detector.detectMarkers(gray)

        # Mostrar información si se detecta un AprilTag
        if apriltags:
            apriltag = apriltags[0]['tag_id']
            obtener_datos(apriltag)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        img = ImageTk.PhotoImage(img)
        panel_camara.imgtk = img
        panel_camara.config(image=img)
        panel_camara.after(10, actualizar_camara)

# Iniciar la cámara
cap = cv2.VideoCapture(0)

# Configurar el detector de AprilTags
detector = cv2.aruco.ArucoDetector()

# Interfaz para obtener datos
app_lectura = tk.Tk()
app_lectura.title("Obtener Datos")

label_resultado = tk.Label(app_lectura, text='')
label_resultado.pack()

# Panel para mostrar la imagen de la cámara
panel_camara = tk.Label(app_lectura)
panel_camara.pack()

# Iniciar la actualización de la cámara
actualizar_camara()

app_lectura.mainloop()

# Liberar recursos de la cámara al cerrar la aplicación
cap.release()
cv2.destroyAllWindows()
