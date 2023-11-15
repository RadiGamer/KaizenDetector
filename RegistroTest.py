import tkinter as tk
import sqlite3
from PIL import Image, ImageTk
from apriltag import apriltag

conn = sqlite3.connect('data.db')
cursor = conn.cursor()
cursor.execute('DROP TABLE IF EXISTS registros')
conn.commit()
conn.close()

conn = sqlite3.connect('data.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS registros (
        tag_id INTEGER PRIMARY KEY,
        nombre TEXT,
        texto_prueba TEXT
    )
''')
conn.commit()
conn.close()

def generar_imagen_apriltag(tag_id):
    # Create a blank image
    tag_img = Image.new('RGB', (200, 200), color='white')
    draw = ImageDraw.Draw(tag_img)

    # Detect AprilTag and draw it on the image
    detector = apriltag.Detector()
    detections = detector.detect(cv2.cvtColor(np.array(tag_img), cv2.COLOR_RGB2GRAY))
    for detection in detections:
        for pt in detection.corners:
            draw.line([tuple(pt[0]), tuple(pt[1])], fill='black', width=3)

    return ImageTk.PhotoImage(tag_img)

def registrar_datos():
    nombre = entry_nombre.get()
    texto_prueba = entry_texto_prueba.get()

    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        cursor.execute('SELECT MAX("tag_id") FROM "registros"')

        result = cursor.fetchone()[0]
        try:
            last_tag_id = int(result) if result is not None else -1
        except (ValueError, TypeError):
            last_tag_id = -1

        conn.close()

        new_tag_id = last_tag_id + 1

        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO "registros" ("tag_id", "nombre", "texto_prueba") VALUES (?, ?, ?)
        ''', (new_tag_id, nombre, texto_prueba))
        conn.commit()
        conn.close()

        image_apriltag = generar_imagen_apriltag(new_tag_id)
        label_imagen_apriltag.config(image=image_apriltag)
        label_imagen_apriltag.image = image_apriltag

        label_resultado.config(text=f'Registro exitoso. Nuevo AprilTag ID: {new_tag_id}')

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

# Label to display the image of the AprilTag
label_imagen_apriltag = tk.Label(app_registro)
label_imagen_apriltag.pack()

app_registro.mainloop()