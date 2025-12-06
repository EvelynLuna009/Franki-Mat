# ventana_ejercicios.py
import tkinter as tk
from tkinter import messagebox
import math
import random
import datetime

from utils_archivos import save_backup
from config import ARCH_RESULTADOS


# ---------------- FUNCIONES AUXILIARES ----------------

def simplificar(num, den):
    if den == 0:
        return (0, 1)
    g = math.gcd(num, den)
    return (num // g, den // g)

def mcm(a, b):
    return abs(a * b) // math.gcd(a, b)


# ---------------- VENTANA DE EJERCICIOS ----------------

class VentanaEjercicios(tk.Toplevel):
    def __init__(self, usuario, ventana_alumno=None):
        super().__init__()
        self.usuario = usuario
        self.ventana_alumno = ventana_alumno   # Para actualizar resultados
        self.title(f"📝 Ejercicios - {usuario}")
        self.geometry("620x520")
        self.configure(bg="#E3F2FD")
        self.resizable(False, False)

        # ---------------- TÍTULOS ----------------
        tk.Label(self, text="Ejercicios de Suma y Resta de Fracciones",
                 font=("Arial", 18, "bold"), bg="#E3F2FD").pack(pady=15)
        tk.Label(self, text="Ingresa tu respuesta en formato a/b (ej. 3/4).",
                 bg="#E3F2FD").pack(pady=5)

        # Pregunta
        self.pregunta_lbl = tk.Label(self, text="", font=("Arial", 20, "bold"), bg="#E3F2FD")
        self.pregunta_lbl.pack(pady=10)

        # Campo de respuesta
        self.entry = tk.Entry(self, width=10, font=("Arial", 16))
        self.entry.pack(pady=10)

        # ---------------- BOTONES PRINCIPALES ----------------
        frame_btns = tk.Frame(self, bg="#E3F2FD")
        frame_btns.pack(pady=10)

        tk.Button(frame_btns, text="Nuevo Ejercicio", width=15, command=self.generar).grid(row=0, column=0, padx=5)
        tk.Button(frame_btns, text="Verificar", width=15, command=self.verificar).grid(row=0, column=1, padx=5)
        tk.Button(frame_btns, text="Pista", width=15, command=self.pista).grid(row=0, column=2, padx=5)

        # ---------------- FEEDBACK ----------------
        self.feedback = tk.Label(self, text="", bg="#E3F2FD", font=("Arial", 12, "bold"))
        self.feedback.pack(pady=5)

        self.pista_lbl = tk.Label(self, text="", bg="#E3F2FD", fg="#457b9d")
        self.pista_lbl.pack(pady=5)

        # ---------------- GUARDAR REGISTRO ----------------
        tk.Button(self, text="💾 Guardar Registro", bg="#C8E6C9",
                  width=20, command=self.guardar_registro).pack(pady=8)

        # ---------------- CONTROLES ----------------
        frame_control = tk.Frame(self, bg="#E3F2FD")
        frame_control.pack(pady=15)

        tk.Button(frame_control, text="🔙 Regresar", bg="#FFF59D",
                  width=15, command=self.destroy).pack(side="left", padx=10)

        tk.Button(frame_control, text="❌ Cerrar sesión", bg="#EF9A9A",
                  width=15, command=self.cerrar_sesion).pack(side="left", padx=10)

        # Primer ejercicio
        self.generar()

    # ---------------- GENERAR EJERCICIO ----------------
    def generar(self):
        self.a = random.randint(1, 7)
        self.b = random.randint(2, 12)
        self.c = random.randint(1, 7)
        self.d = random.randint(2, 12)
        self.oper = random.choice(["+", "-"])

        # Evitar resultado negativo
        if self.oper == "-" and self.a / self.b < self.c / self.d:
            self.a, self.b, self.c, self.d = self.c, self.d, self.a, self.b

        self.pregunta_lbl.config(text=f"{self.a}/{self.b} {self.oper} {self.c}/{self.d}")

        m = mcm(self.b, self.d)
        n1 = self.a * (m // self.b)
        n2 = self.c * (m // self.d)

        res = n1 + n2 if self.oper == "+" else n1 - n2

        self.respuesta = simplificar(res, m)

        self.entry.delete(0, tk.END)
        self.feedback.config(text="")
        self.pista_lbl.config(text="")

    # ---------------- VERIFICAR RESPUESTA ----------------
    def verificar(self):
        try:
            p, q = map(int, self.entry.get().split("/"))
            if simplificar(p, q) == self.respuesta:
                self.feedback.config(text="✔ Correcto", fg="green")
            else:
                self.feedback.config(text=f"✘ Incorrecto — Correcta: {self.respuesta[0]}/{self.respuesta[1]}",
                                     fg="red")
        except:
            self.feedback.config(text="Formato incorrecto (usa a/b)", fg="orange")

    # ---------------- PISTA ----------------
    def pista(self):
        self.pista_lbl.config(text=f"Pista: m.c.m. de {self.b} y {self.d}")

    # ---------------- GUARDAR REGISTRO ----------------
    def guardar_registro(self):
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        operacion = f"{self.a}/{self.b} {self.oper} {self.c}/{self.d}"
        resultado = f"{self.respuesta[0]}/{self.respuesta[1]}"
        intento = "1/1"

        save_backup(ARCH_RESULTADOS)

        with open(ARCH_RESULTADOS, "a", encoding="utf-8") as f:
            f.write(f"{fecha}|{self.usuario}|Ejercicios|{operacion} = {resultado}|{intento}\n")

        messagebox.showinfo("Guardado", "Registro guardado correctamente.")

        # ACTUALIZAR LISTA DE RESULTADOS EN TIEMPO REAL
        if self.ventana_alumno:
            self.ventana_alumno.ver_resultados()

    # ---------------- CERRAR SESIÓN ----------------
    def cerrar_sesion(self):
        if messagebox.askyesno("Cerrar sesión", "¿Deseas cerrar la sesión?"):
            self.destroy()
            try:
                self.master.destroy()
            except:
                pass
