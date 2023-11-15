import tkinter as tk
import cv2
from tkinter import PhotoImage
import sqlite3
from PIL import Image, ImageTk

def obtener_datos(aruco_id):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM registros WHERE aruco_id = ?', (aruco_id,))
    data = cursor.fetchone()
    conn.close()

    if data:
        resultado = f"Nombre: {data[2]}\nTexto de Prueba: {data[3]}"
    else:
        resultado = "ArUco Tag not found"

    label_resultado.config(text=resultado)

# Function to update the camera image
def actualizar_camara():
    ret, frame = cap.read()
    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect ArUco Tags
        corners, ids, rejectedImgPoints = cv2.aruco.CharucoDetector()

        # Display information if an ArUco Tag is detected
        if ids is not None and len(ids) > 0:
            aruco_id = ids[0]
            obtener_datos(aruco_id)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        img = ImageTk.PhotoImage(img)
        panel_camara.imgtk = img
        panel_camara.config(image=img)
        panel_camara.after(10, actualizar_camara)

# Start the camera
cap = cv2.VideoCapture(0)

# Configure the ArUco dictionary
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

# Tkinter interface to get data
app_lectura = tk.Tk()
app_lectura.title("Get Data")

label_resultado = tk.Label(app_lectura, text='')
label_resultado.pack()

# Panel to display the camera image
panel_camara = tk.Label(app_lectura)
panel_camara.pack()

# Start updating the camera
actualizar_camara()

app_lectura.mainloop()

# Release camera resources upon application exit
cap.release()
cv2.destroyAllWindows()
