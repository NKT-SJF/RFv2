
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import subprocess
import os
import shutil
import sys

# Rutas
BASE = r'C:\Users\THN_LAB\Desktop\RF1\Reconocimiento Facial'
CODE = os.path.join(BASE, 'code')
DATA = os.path.join(BASE, 'Data')

def mostrar_resultado(resultado):
    texto_resultado.delete("1.0", tk.END)
    texto_resultado.insert(tk.END, resultado)

def ejecutar_script(script, argumentos=None):
    ruta = os.path.join(CODE, script)

    if not os.path.exists(ruta):
        mostrar_resultado("No se encontró el archivo:\n" + ruta)
        return

    try:
        comando = [sys.executable, ruta]
        if argumentos:
            comando.extend(argumentos)

        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )

        salida = resultado.stdout
        if resultado.stderr:
            salida += "\nERRORES:\n" + resultado.stderr

        mostrar_resultado(salida or "Proceso finalizado.")

    except Exception as e:
        mostrar_resultado(f"Error: {str(e)}")

def ejF():
    nombre = entry_nombre.get().strip()

    if not nombre:
        mostrar_resultado("Por favor ingrese un nombre.")
        return

    ejecutar_script("Faces.py", [nombre])
    entry_nombre.delete(0, tk.END)

def ejRF():
    ejecutar_script("FacialRecognizer.py")

def ejMRF():
    ejecutar_script("ModelsFaceRecognizer.py")

def DU():
    nombre = entry_nombre.get().strip()

    if not nombre:
        mostrar_resultado("Ingrese el nombre de la carpeta.")
        return

    carpeta = os.path.join(DATA, nombre)

    if not os.path.isdir(carpeta):
        mostrar_resultado("La carpeta no existe.")
        return

    confirmar = messagebox.askyesno(
        "Confirmar eliminación",
        f"¿Desea eliminar la carpeta {nombre}?"
    )

    if confirmar:
        try:
            shutil.rmtree(carpeta)
            mostrar_resultado(
                f"Carpeta '{nombre}' eliminada correctamente."
            )
            entry_nombre.delete(0, tk.END)

        except Exception as e:
            mostrar_resultado(f"Error: {str(e)}")

# Ventana principal
ventana = tk.Tk()
ventana.title("Sistema de Reconocimiento Facial")
ventana.geometry("1100x700")
ventana.minsize(800, 550)
ventana.configure(bg="#F1F5F9")

# Configuración de columnas
ventana.grid_columnconfigure(0, weight=1)
ventana.grid_columnconfigure(1, weight=3)
ventana.grid_rowconfigure(1, weight=1)

# Encabezado
header = tk.Frame(ventana, bg="#172B4D", height=75)
header.grid(row=0, column=0, columnspan=2, sticky="nsew")
header.grid_propagate(False)

titulo = tk.Label(
    header,
    text="SISTEMA DE RECONOCIMIENTO FACIAL",
    font=("Segoe UI", 18, "bold"),
    bg="#172B4D",
    fg="white"
)
titulo.pack(side="left", padx=25, pady=20)

# Panel izquierdo
panel = tk.Frame(ventana, bg="#E2E8F0", padx=20, pady=20)
panel.grid(row=1, column=0, sticky="nsew")

tk.Label(
    panel,
    text="PANEL DE CONTROL",
    font=("Segoe UI", 13, "bold"),
    bg="#E2E8F0",
    fg="#172B4D"
).pack(pady=(5, 20))

tk.Label(
    panel,
    text="Nombre de persona:",
    font=("Segoe UI", 10),
    bg="#E2E8F0"
).pack(anchor="w")

entry_nombre = tk.Entry(
    panel,
    font=("Segoe UI", 12),
    relief="flat",
    bd=5
)
entry_nombre.pack(fill="x", ipady=8, pady=(5, 20))

def crear_boton(texto, funcion, color="#2563EB"):
    boton = tk.Button(
        panel,
        text=texto,
        command=funcion,
        font=("Segoe UI", 10, "bold"),
        bg=color,
        fg="white",
        activebackground="#1D4ED8",
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        pady=12
    )
    boton.pack(fill="x", pady=7)

crear_boton("Captura de cara", ejF)
crear_boton("Reconocimiento facial", ejRF)
crear_boton("Entrenar modelo", ejMRF)
crear_boton("Borrar subcarpeta", DU, "#DC2626")

# Panel derecho
contenido = tk.Frame(ventana, bg="#F8FAFC", padx=20, pady=20)
contenido.grid(row=1, column=1, sticky="nsew")

contenido.grid_rowconfigure(1, weight=1)
contenido.grid_columnconfigure(0, weight=1)

tk.Label(
    contenido,
    text="CONSOLA DE RESULTADOS",
    font=("Segoe UI", 14, "bold"),
    bg="#F8FAFC",
    fg="#172B4D"
).grid(row=0, column=0, sticky="w", pady=(0, 15))

texto_resultado = scrolledtext.ScrolledText(
    contenido,
    font=("Consolas", 10),
    bg="#FFFFFF",
    fg="#334155",
    insertbackground="#172B4D",
    relief="flat",
    wrap=tk.WORD,
    padx=12,
    pady=12
)
texto_resultado.grid(row=1, column=0, sticky="nsew")

texto_resultado.insert(
    tk.END,
    "Sistema iniciado correctamente.\n"
    "Seleccione una operación en el panel izquierdo."
)

ventana.mainloop()
