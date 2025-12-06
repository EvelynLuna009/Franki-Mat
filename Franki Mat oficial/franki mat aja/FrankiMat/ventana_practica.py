import tkinter as tk
from tkinter import messagebox
import math

def simplificar(num, den):
    """Simplifica una fracción"""
    if den == 0:
        return (0, 1)
    g = math.gcd(num, den)
    return (num//g, den//g)

def mcm(a, b):
    """Calcula el mínimo común múltiplo"""
    return abs(a*b) // math.gcd(a, b)

class VentanaPractica(tk.Toplevel):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.title(f"🎮 Práctica - {usuario}")
        self.geometry("600x500")
        self.configure(bg="#E3F2FD")
        self.resizable(False, False)

        tk.Label(self, text="Suma y Resta de Fracciones",
                 font=("Arial", 18, "bold"), bg="#E3F2FD").pack(pady=12)
        tk.Label(self, text="Ingresa tu respuesta en formato a/b (ej. 3/4).",
                 bg="#E3F2FD").pack(pady=5)

        # Frame para mostrar la operación
        self.frame_operacion = tk.Frame(self, bg="#E3F2FD")
        self.frame_operacion.pack(pady=10)

        self.pregunta_lbl = tk.Label(self.frame_operacion, text="", font=("Arial", 20, "bold"), bg="#E3F2FD")
        self.pregunta_lbl.pack()

        # Entry para que el usuario ingrese la respuesta
        self.entry = tk.Entry(self, width=10, font=("Arial", 16))
        self.entry.pack(pady=10)

        # Botones de control
        frame_btns = tk.Frame(self, bg="#E3F2FD")
        frame_btns.pack(pady=10)
        tk.Button(frame_btns, text="Nuevo Ejercicio", width=15, command=self.generar).grid(row=0, column=0, padx=5)
        tk.Button(frame_btns, text="Verificar", width=15, command=self.verificar).grid(row=0, column=1, padx=5)
        tk.Button(frame_btns, text="Pista", width=15, command=self.pista).grid(row=0, column=2, padx=5)

        # Feedback
        self.feedback = tk.Label(self, text="", bg="#E3F2FD", font=("Arial", 12, "bold"))
        self.feedback.pack(pady=5)

        self.pista_lbl = tk.Label(self, text="", bg="#E3F2FD", fg="#457b9d")
        self.pista_lbl.pack(pady=5)

        # Botones de cerrar y regresar
        frame_control = tk.Frame(self, bg="#E3F2FD")
        frame_control.pack(pady=15)
        tk.Button(frame_control, text="🔙 Regresar", bg="#FFF59D", width=15, command=self.destroy).pack(side="left", padx=10)
        tk.Button(frame_control, text="❌ Cerrar sesión", bg="#EF9A9A", width=15, command=self.cerrar_sesion).pack(side="left", padx=10)

        self.generar()

    def generar(self):
        """Genera una operación aleatoria de suma o resta"""
        import random
        self.a = random.randint(1, 7)
        self.b = random.randint(2, 12)
        self.c = random.randint(1, 7)
        self.d = random.randint(2, 12)
        self.oper = random.choice(["+", "-"])

        # Evitar resultado negativo
        if self.oper == "-" and self.a/self.b < self.c/self.d:
            self.a, self.b, self.c, self.d = self.c, self.d, self.a, self.b

        self.pregunta_lbl.config(text=f"{self.a}/{self.b} {self.oper} {self.c}/{self.d}")

        # Calcular la respuesta correcta
        m = mcm(self.b, self.d)
        n1 = self.a * (m // self.b)
        n2 = self.c * (m // self.d)
        res = n1 + n2 if self.oper == "+" else n1 - n2
        self.respuesta = simplificar(res, m)

        self.entry.delete(0, tk.END)
        self.feedback.config(text="")
        self.pista_lbl.config(text="")

    def verificar(self):
        """Verifica la respuesta ingresada por el usuario"""
        try:
            p, q = map(int, self.entry.get().split("/"))
            if simplificar(p, q) == self.respuesta:
                self.feedback.config(text="✔ Correcto", fg="green")
            else:
                self.feedback.config(text=f"✘ Incorrecto — Correcta: {self.respuesta[0]}/{self.respuesta[1]}", fg="red")
        except:
            self.feedback.config(text="Formato incorrecto (usa a/b)", fg="orange")

    def pista(self):
        """Muestra una pista sobre cómo resolver la operación"""
        self.pista_lbl.config(text=f"Pista: encuentra el m.c.m. de {self.b} y {self.d} para operar.")

    def cerrar_sesion(self):
        """Cierra la ventana de práctica y termina sesión"""
        if messagebox.askyesno("Cerrar sesión", "¿Deseas cerrar la sesión?"):
            self.destroy()
            try:
                self.master.destroy()  # opcional: cerrar la ventana principal
            except:
                pass
