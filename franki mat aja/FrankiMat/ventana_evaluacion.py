# ventana_evaluacion.py
import tkinter as tk
from tkinter import messagebox
import random
import math
from datetime import datetime
from config import ARCH_RESULTADOS


def simplificar(num, den):
    g = math.gcd(num, den)
    return num // g, den // g


class VentanaEvaluacion(tk.Toplevel):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario

        self.title("Evaluación")
        self.geometry("650x600")
        self.config(bg="#FCE4EC")
        self.resizable(False, False)

        tk.Label(self, text="Evaluación Final",
                 font=("Arial", 26, "bold"),
                 bg="#FCE4EC").pack(pady=20)

        tk.Label(self, text="Selecciona cuántas preguntas quieres responder:",
                 font=("Arial", 14), bg="#FCE4EC").pack(pady=10)

        frame = tk.Frame(self, bg="#FCE4EC")
        frame.pack()

        # Botones de selección
        tk.Button(frame, text="5 preguntas", width=14, font=("Arial", 12),
                  command=lambda: self.iniciar_examen(5)).grid(row=0, column=0, padx=10)

        tk.Button(frame, text="10 preguntas", width=14, font=("Arial", 12),
                  command=lambda: self.iniciar_examen(10)).grid(row=0, column=1, padx=10)

        tk.Button(frame, text="15 preguntas", width=14, font=("Arial", 12),
                  command=lambda: self.iniciar_examen(15)).grid(row=0, column=2, padx=10)

        tk.Button(frame, text="20 preguntas", width=14, font=("Arial", 12),
                  command=lambda: self.iniciar_examen(20)).grid(row=0, column=3, padx=10)

        self.examen_iniciado = False

    # ---------------------------------------------------------
    # INICIAR EXAMEN
    # ---------------------------------------------------------
    def iniciar_examen(self, cantidad):
        self.cantidad_preguntas = cantidad
        self.pregunta_actual = 0
        self.correctas = 0
        self.lista_preguntas = []

        # Ocultar selección inicial
        for widget in self.winfo_children():
            widget.pack_forget()

        self.generar_preguntas()

        # Interfaz del examen
        self.lbl_info = tk.Label(self, text=f"Pregunta 1 de {self.cantidad_preguntas}",
                                 font=("Arial", 16), bg="#FCE4EC")
        self.lbl_info.pack(pady=10)

        self.lbl_pregunta = tk.Label(self, text="", font=("Arial", 22, "bold"), bg="#FCE4EC")
        self.lbl_pregunta.pack(pady=20)

        self.entry = tk.Entry(self, font=("Arial", 20), width=10)
        self.entry.pack()

        frame = tk.Frame(self, bg="#FCE4EC")
        frame.pack(pady=20)

        tk.Button(frame, text="Verificar", font=("Arial", 14),
                  command=self.verificar).grid(row=0, column=0, padx=10)

        tk.Button(frame, text="Siguiente", font=("Arial", 14),
                  command=self.siguiente).grid(row=0, column=1, padx=10)

        tk.Button(frame, text="Guardar registro", font=("Arial", 14),
                  command=self.guardar_registro).grid(row=0, column=2, padx=10)

        self.lbl_feedback = tk.Label(self, text="", font=("Arial", 16),
                                     bg="#FCE4EC")
        self.lbl_feedback.pack(pady=15)

        tk.Button(self, text="Regresar", bg="#FFF59D",
                  font=("Arial", 12), width=15,
                  command=self.destroy).pack(pady=10)

        self.mostrar_pregunta()

    # ---------------------------------------------------------
    # GENERAR PREGUNTAS
    # ---------------------------------------------------------
    def generar_preguntas(self):
        for _ in range(self.cantidad_preguntas):
            a = random.randint(1, 9)
            b = random.randint(2, 12)
            c = random.randint(1, 9)
            d = random.randint(2, 12)

            oper = random.choice(["+", "-"])

            # evitar resultado negativo
            if oper == "-" and a/b < c/d:
                a, b, c, d = c, d, a, b

            # respuesta correcta
            m = (b * d) // math.gcd(b, d)
            n1 = a * (m // b)
            n2 = c * (m // d)
            res = n1 + n2 if oper == "+" else n1 - n2
            correcta = simplificar(res, m)

            pregunta = {
                "a": a, "b": b,
                "c": c, "d": d,
                "oper": oper,
                "correcta": correcta
            }
            self.lista_preguntas.append(pregunta)

    # ---------------------------------------------------------
    # MOSTRAR PREGUNTA
    # ---------------------------------------------------------
    def mostrar_pregunta(self):
        p = self.lista_preguntas[self.pregunta_actual]
        self.lbl_pregunta.config(text=f"{p['a']}/{p['b']} {p['oper']} {p['c']}/{p['d']}")
        self.lbl_info.config(text=f"Pregunta {self.pregunta_actual + 1} de {self.cantidad_preguntas}")
        self.entry.delete(0, tk.END)
        self.lbl_feedback.config(text="")

    # ---------------------------------------------------------
    # VERIFICAR RESPUESTA
    # ---------------------------------------------------------
    def verificar(self):
        try:
            p, q = map(int, self.entry.get().split("/"))
            respuesta = simplificar(p, q)

            correcta = self.lista_preguntas[self.pregunta_actual]["correcta"]

            if respuesta == correcta:
                self.lbl_feedback.config(text="✔ Correcto", fg="green")
                self.correctas += 1
            else:
                self.lbl_feedback.config(text=f"✘ Incorrecto (correcto: {correcta[0]}/{correcta[1]})",
                                         fg="red")
        except:
            self.lbl_feedback.config(text="Formato inválido. Usa a/b", fg="orange")

    # ---------------------------------------------------------
    # SIGUIENTE PREGUNTA
    # ---------------------------------------------------------
    def siguiente(self):
        if self.pregunta_actual < self.cantidad_preguntas - 1:
            self.pregunta_actual += 1
            self.mostrar_pregunta()
        else:
            self.finalizar_examen()

    # ---------------------------------------------------------
    # FINAL DEL EXAMEN
    # ---------------------------------------------------------
    def finalizar_examen(self):
        self.lbl_pregunta.config(text="")
        self.entry.pack_forget()

        self.lbl_info.config(text="Examen finalizado")
        self.lbl_feedback.config(text=f"Puntaje: {self.correctas}/{self.cantidad_preguntas}",
                                 fg="blue")

    # ---------------------------------------------------------
    # GUARDAR REGISTRO
    # ---------------------------------------------------------
    def guardar_registro(self):
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        resultado = f"{self.correctas}/{self.cantidad_preguntas}"

        linea = f"{fecha}|{self.usuario}|Examen|{resultado}|---\n"

        with open(ARCH_RESULTADOS, "a", encoding="utf-8") as f:
            f.write(linea)

        messagebox.showinfo("Guardado", "Registro almacenado correctamente.")
