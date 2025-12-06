# modulo_practica_simple.py
import tkinter as tk
from tkinter import messagebox
import random
import math

def simplificar(num, den):
    if den == 0:
        return (0,1)
    g = math.gcd(num, den)
    return (num//g, den//g)

def mcm(a,b):
    return abs(a*b)//math.gcd(a,b)

class ModuloPracticaSimple(tk.Toplevel):
    def __init__(self, master, alumno=None):
        super().__init__(master)
        self.alumno = alumno
        self.title("🎮 Módulo de Práctica (Suma/Resta)")
        self.geometry("700x420")
        self.config(bg="#e8f6ef")
        self.resizable(False, False)

        tk.Label(self, text="Practica suma y resta de fracciones",
                 font=("Comic Sans MS", 18, "bold"),
                 bg="#e8f6ef").pack(pady=10)
        tk.Label(self, text="Responde en formato a/b (ej. 3/4).",
                 bg="#e8f6ef").pack()

        self.pregunta_lbl = tk.Label(self, text="", font=("Arial", 24, "bold"), bg="#e8f6ef")
        self.pregunta_lbl.pack(pady=12)

        self.entry = tk.Entry(self, width=10, font=("Arial", 16))
        self.entry.pack()

        btns = tk.Frame(self, bg="#e8f6ef")
        btns.pack(pady=8)
        tk.Button(btns, text="Nuevo", width=12, command=self.generar).grid(row=0, column=0, padx=6)
        tk.Button(btns, text="Verificar", width=12, command=self.verificar).grid(row=0, column=1, padx=6)
        tk.Button(btns, text="Pista", width=12, command=self.pista).grid(row=0, column=2, padx=6)

        self.feedback = tk.Label(self, text="", bg="#e8f6ef", font=("Arial", 12))
        self.feedback.pack(pady=6)
        self.pista_lbl = tk.Label(self, text="", bg="#e8f6ef", fg="#457b9d")
        self.pista_lbl.pack()

        tk.Button(self, text="🔙 Regresar", bg="#ffd6a5", width=18, command=self.destroy).pack(side="bottom", pady=10)

        self.generar()

    def generar(self):
        self.a = random.randint(1, 7)
        self.b = random.randint(2, 12)
        self.c = random.randint(1, 7)
        self.d = random.randint(2, 12)
        self.oper = random.choice(["+", "-"])
        # avoid negative results
        if self.oper == "-" and self.a/self.b < self.c/self.d:
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

    def verificar(self):
        try:
            p,q = map(int, self.entry.get().split("/"))
            if simplificar(p,q) == self.respuesta:
                self.feedback.config(text="✔ Correcto", fg="green")
            else:
                self.feedback.config(text=f"✘ Incorrecto — Correcta: {self.respuesta[0]}/{self.respuesta[1]}", fg="red")
        except:
            self.feedback.config(text="Formato incorrecto (usa a/b)", fg="orange")

    def pista(self):
        self.pista_lbl.config(text=f"Pista: encuentra el m.c.m. de {self.b} y {self.d}.")
