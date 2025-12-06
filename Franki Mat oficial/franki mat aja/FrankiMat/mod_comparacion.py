# modulo_comparacion.py
import tkinter as tk
from tkinter import messagebox

class ModuloComparacion(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("🔢 Módulo de Comparación")
        self.geometry("660x340")
        self.config(bg="#f0f7ff")
        self.resizable(False, False)

        tk.Label(self, text="Compara dos fracciones",
                 font=("Comic Sans MS", 18, "bold"),
                 bg="#f0f7ff").pack(pady=12)
        tk.Label(self, text="Ingresa dos fracciones válidas (ej. 1/2 y 3/4):",
                 bg="#f0f7ff").pack()

        frm = tk.Frame(self, bg="#f0f7ff")
        frm.pack(pady=10)

        self.e1 = tk.Entry(frm, width=6); self.e1.grid(row=0, column=0)
        tk.Label(frm, text="/", bg="#f0f7ff").grid(row=0, column=1)
        self.e2 = tk.Entry(frm, width=6); self.e2.grid(row=0, column=2)

        tk.Label(frm, text="   y   ", bg="#f0f7ff").grid(row=0, column=3)

        self.e3 = tk.Entry(frm, width=6); self.e3.grid(row=0, column=4)
        tk.Label(frm, text="/", bg="#f0f7ff").grid(row=0, column=5)
        self.e4 = tk.Entry(frm, width=6); self.e4.grid(row=0, column=6)

        tk.Button(self, text="Comparar", width=16, command=self.comparar, bg="#bbdefb").pack(pady=12)
        self.res_lbl = tk.Label(self, text="", bg="#f0f7ff", font=("Arial", 14))
        self.res_lbl.pack(pady=6)

        tk.Button(self, text="🔙 Regresar", width=18, bg="#ffd6a5", command=self.destroy).pack(pady=8)

    def comparar(self):
        try:
            a = int(self.e1.get()); b = int(self.e2.get()); c = int(self.e3.get()); d = int(self.e4.get())
            if b == 0 or d == 0:
                raise ValueError
            if a*d == b*c:
                self.res_lbl.config(text="✔ Son equivalentes", fg="green")
            elif a/b > c/d:
                self.res_lbl.config(text="La primera fracción es mayor.", fg="blue")
            else:
                self.res_lbl.config(text="La segunda fracción es mayor.", fg="blue")
        except:
            self.res_lbl.config(text="Ingresa fracciones válidas (ej. 1/2 y 3/4).", fg="red")
