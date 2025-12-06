import tkinter as tk
from tkinter import messagebox

class VentanaComparacion(tk.Toplevel):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.title(f"🔍 Comparación de Fracciones - {usuario}")
        self.geometry("600x400")
        self.configure(bg="#E3F2FD")
        self.resizable(False, False)

        # Título
        tk.Label(self, text="Comparar Fracciones",
                 font=("Arial", 18, "bold"), bg="#E3F2FD").pack(pady=20)
        tk.Label(self, text="Ingresa las fracciones en formato a/b (ej. 3/4).",
                 bg="#E3F2FD").pack(pady=5)

        # Frame para las entradas
        frame_entry = tk.Frame(self, bg="#E3F2FD")
        frame_entry.pack(pady=15)

        tk.Label(frame_entry, text="Fracción 1:", bg="#E3F2FD").grid(row=0, column=0, padx=5, pady=5)
        self.frac1 = tk.Entry(frame_entry, width=8, font=("Arial", 14))
        self.frac1.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_entry, text="Fracción 2:", bg="#E3F2FD").grid(row=1, column=0, padx=5, pady=5)
        self.frac2 = tk.Entry(frame_entry, width=8, font=("Arial", 14))
        self.frac2.grid(row=1, column=1, padx=5, pady=5)

        # Botones
        frame_btns = tk.Frame(self, bg="#E3F2FD")
        frame_btns.pack(pady=10)

        tk.Button(frame_btns, text="Comparar", width=12, command=self.comparar).grid(row=0, column=0, padx=5)
        tk.Button(frame_btns, text="Nuevo", width=12, command=self.nuevo).grid(row=0, column=1, padx=5)
        tk.Button(frame_btns, text="🔙 Regresar", width=12, bg="#FFF59D", command=self.destroy).grid(row=0, column=2, padx=5)

        # Label para mostrar resultado
        self.resultado_lbl = tk.Label(self, text="", font=("Arial", 14, "bold"), bg="#E3F2FD")
        self.resultado_lbl.pack(pady=15)

    def comparar(self):
        """Compara las dos fracciones ingresadas"""
        try:
            n1, d1 = map(int, self.frac1.get().split("/"))
            n2, d2 = map(int, self.frac2.get().split("/"))
            if d1 == 0 or d2 == 0:
                raise ValueError
            val1 = n1 / d1
            val2 = n2 / d2
            if val1 > val2:
                self.resultado_lbl.config(text=f"{n1}/{d1} > {n2}/{d2}", fg="green")
            elif val1 < val2:
                self.resultado_lbl.config(text=f"{n1}/{d1} < {n2}/{d2}", fg="red")
            else:
                self.resultado_lbl.config(text=f"{n1}/{d1} = {n2}/{d2}", fg="blue")
        except:
            self.resultado_lbl.config(text="Formato incorrecto. Usa a/b", fg="orange")

    def nuevo(self):
        """Limpia los campos y resultado para un nuevo intento"""
        self.frac1.delete(0, tk.END)
        self.frac2.delete(0, tk.END)
        self.resultado_lbl.config(text="")
