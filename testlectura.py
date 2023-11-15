import cv2
import tkinter as tk
from PIL import Image, ImageTk

# Configuración de la cámara
cap = cv2.VideoCapture(0)

# Configuración del detector de AprilTags
detector = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters()

# Función para actualizar la interfaz con la información del AprilTag
def update_interface(tag_id):
    label.config(text=f"AprilTag ID: {tag_id}")

# Función para capturar y procesar los fotogramas de la cámara
def capture_frames():
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, detector, parameters=parameters)

    if ids is not None:
        for i in range(len(ids)):
            # Actualiza la interfaz con la información del AprilTag
            update_interface(int(ids[i][0]))

            # Dibuja un rectángulo alrededor del AprilTag en la imagen
            cv2.aruco.drawDetectedMarkers(frame, corners)

    # Convierte la imagen para mostrarla en la interfaz
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(image)
    img = ImageTk.PhotoImage(image=img)

    # Actualiza la etiqueta en la interfaz con el nuevo fotograma
    panel.img = img
    panel.config(image=img)

    # Programa la función para el próximo fotograma
    panel.after(10, capture_frames)

# Configuración de la interfaz
root = tk.Tk()
root.title("AprilTag Interface")

# Etiqueta para mostrar el ID del AprilTag
label = tk.Label(root, text="AprilTag ID: ")
label.pack()

# Panel para mostrar la imagen de la cámara
panel = tk.Label(root)
panel.pack()

# Inicia el proceso de captura de fotogramas
capture_frames()

# Ejecuta la interfaz
root.mainloop()

# Libera los recursos
cap.release()
cv2.destroyAllWindows()
