import tkinter as tk
from tkinter import messagebox
from config import ARCH_RESULTADOS, ARCH_ALUMNOS
from utils_archivos import read_lines_safe


class VentanaMaestro(tk.Toplevel):
    def __init__(self, usuario):
        super().__init__()

        self.usuario = usuario
        self.title(f"Panel Maestro - {usuario}")
        self.geometry("500x520")
        self.configure(bg="#E8F0FE")
        self.resizable(False, False)

        # --------------------------
        # TITULO
        # --------------------------
        tk.Label(
            self,
            text=f"Bienvenido, Maestra {usuario}",
            font=("Comic Sans MS", 24, "bold"),
            bg="#E8F0FE",
            fg="#003566"
        ).pack(pady=30)

        # --------------------------
        # BOTONES PRINCIPALES
        # --------------------------
        tk.Button(
            self,
            text="📘 Ver historial completo de alumnos",
            font=("Arial", 14),
            width=32,
            bg="#90CAF9",
            command=self.ver_historial_completo
        ).pack(pady=12)

        tk.Button(
            self,
            text="📗 Ver historial por alumno",
            font=("Arial", 14),
            width=32,
            bg="#A5D6A7",
            command=self.ver_historial_por_alumno
        ).pack(pady=12)

        tk.Button(
            self,
            text="🔙 Regresar",
            font=("Arial", 14),
            width=20,
            bg="#FFF59D",
            command=self.regresar
        ).pack(pady=15)

        tk.Button(
            self,
            text="❌ Cerrar sesión",
            font=("Arial", 14),
            width=20,
            bg="#EF9A9A",
            command=self.cerrar_sesion
        ).pack(pady=10)

    # ---------------------------------------------------------
    # FUNCIÓN: Ver historial completo
    # ---------------------------------------------------------
    def ver_historial_completo(self):
        ventana = tk.Toplevel(self)
        ventana.title("Historial completo de alumnos")
        ventana.geometry("600x500")
        ventana.config(bg="#FFFFFF")

        tk.Label(
            ventana,
            text="Historial completo",
            font=("Arial", 18, "bold"),
            bg="#FFFFFF"
        ).pack(pady=15)

        texto = tk.Text(ventana, width=70, height=20)
        texto.pack(pady=10)

        lineas = read_lines_safe(ARCH_RESULTADOS)

        if not lineas:
            texto.insert(tk.END, "No hay registros aún.")
        else:
            for linea in lineas:
                texto.insert(tk.END, linea + "\n")

    # ---------------------------------------------------------
    # FUNCIÓN: Ver historial por alumno
    # ---------------------------------------------------------
    def ver_historial_por_alumno(self):
        ventana = tk.Toplevel(self)
        ventana.title("Consultar historial por alumno")
        ventana.geometry("500x400")
        ventana.config(bg="#FFFFFF")

        tk.Label(
            ventana,
            text="Selecciona un alumno:",
            font=("Arial", 15, "bold"),
            bg="#FFFFFF"
        ).pack(pady=10)

        lista = tk.Listbox(ventana, width=40, height=15)
        lista.pack(pady=10)

        # Cargar alumnos desde archivo
        alumnos = [line.split("|")[0] for line in read_lines_safe(ARCH_ALUMNOS)]

        for alumno in alumnos:
            lista.insert(tk.END, alumno)

        # --- Botón ver ---
        def mostrar():
            seleccionado = lista.get(tk.ACTIVE)
            if not seleccionado:
                messagebox.showwarning("Atención", "Debe seleccionar un alumno.")
                return

            self.mostrar_historial_individual(seleccionado)

        tk.Button(
            ventana,
            text="Ver historial",
            bg="#90CAF9",
            width=20,
            command=mostrar
        ).pack(pady=10)

    # ---------------------------------------------------------
    # FUNCIÓN CORREGIDA: Mostrar historial individual
    # ---------------------------------------------------------
    def mostrar_historial_individual(self, alumno):
        ventana = tk.Toplevel(self)
        ventana.title(f"Historial de {alumno}")
        ventana.geometry("650x520")
        ventana.config(bg="#FFFFFF")

        tk.Label(
            ventana,
            text=f"Historial de: {alumno}",
            font=("Arial", 18, "bold"),
            bg="#FFFFFF"
        ).pack(pady=15)

        texto = tk.Text(ventana, width=80, height=22)
        texto.pack(pady=10)

        # --- CORRECCIÓN IMPORTANTE ---
        # Antes solo filtraba si la línea empezaba EXACTO con "Nombre|"
        # Pero tus registros de evaluación y ejercicios NO siempre empiezan así.
        # Ahora filtramos si el alumno aparece en la línea.
        registros = [
            linea for linea in read_lines_safe(ARCH_RESULTADOS)
            if alumno.lower() in linea.lower()
        ]

        if registros:
            for reg in registros:
                texto.insert(tk.END, reg + "\n")
        else:
            texto.insert(tk.END, "Este alumno no tiene registros aún.")

    # ---------------------------------------------------------
    # BOTÓN REGRESAR
    # ---------------------------------------------------------
    def regresar(self):
        self.destroy()

    # ---------------------------------------------------------
    # BOTÓN CERRAR SESIÓN
    # ---------------------------------------------------------
    def cerrar_sesion(self):
        messagebox.showinfo("Sesión cerrada", "La sesión ha sido cerrada.")
        self.destroy()
