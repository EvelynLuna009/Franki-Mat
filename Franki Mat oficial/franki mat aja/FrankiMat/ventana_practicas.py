import tkinter as tk
from tkinter import messagebox


class VentanaPracticas(tk.Toplevel):
    def __init__(self, usuario):
        super().__init__()

        self.usuario = usuario
        self.title(f"Prácticas - {usuario}")
        self.geometry("520x520")
        self.configure(bg="#F0F7FF")
        self.resizable(False, False)

        # -------------------------
        # TÍTULO
        # -------------------------
        tk.Label(
            self,
            text="PRÁCTICAS",
            font=("Comic Sans MS", 26, "bold"),
            fg="#003566",
            bg="#F0F7FF"
        ).pack(pady=25)

        # -------------------------
        # BOTONES PRINCIPALES
        # -------------------------
        tk.Button(
            self,
            text="📘 Aprendizaje",
            font=("Arial", 16),
            width=25,
            bg="#90CAF9",
            command=self.modulo_aprendizaje
        ).pack(pady=12)

        tk.Button(
            self,
            text="📝 Práctica",
            font=("Arial", 16),
            width=25,
            bg="#A5D6A7",
            command=self.modulo_practica
        ).pack(pady=12)

        tk.Button(
            self,
            text="📊 Comparación",
            font=("Arial", 16),
            width=25,
            bg="#FFF59D",
            command=self.modulo_comparacion
        ).pack(pady=12)

        tk.Button(
            self,
            text="🧠 Evaluación",
            font=("Arial", 16),
            width=25,
            bg="#EF9A9A",
            command=self.modulo_evaluacion
        ).pack(pady=12)

        # -------------------------
        # BOTONES INFERIORES
        # -------------------------
        tk.Button(
            self,
            text="🔙 Regresar",
            font=("Arial", 14),
            width=18,
            bg="#B0BEC5",
            command=self.regresar
        ).pack(pady=20)

        tk.Button(
            self,
            text="❌ Cerrar ventana",
            font=("Arial", 14),
            width=18,
            bg="#FF8A80",
            command=self.destroy
        ).pack()

    # ---------------------------------------------------------
    # MÓDULOS (conectarás tus ejercicios aquí)
    # ---------------------------------------------------------
    def modulo_aprendizaje(self):
        messagebox.showinfo("Aprendizaje", "Aquí irá el módulo de aprendizaje.\nSi quieres, te lo programo.")

    def modulo_practica(self):
        messagebox.showinfo("Práctica", "Aquí irán las actividades de práctica.\nListo para agregar ejercicios.")

    def modulo_comparacion(self):
        messagebox.showinfo("Comparación", "Aquí irá el módulo de comparación.")

    def modulo_evaluacion(self):
        messagebox.showinfo("Evaluación", "Aquí irá el examen o evaluación final.")

    # ---------------------------------------------------------
    def regresar(self):
        self.destroy()
