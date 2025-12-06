# modulo_aprendizaje.py
import tkinter as tk
import math

class ModuloAprendizaje(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("📘 Módulo de Aprendizaje")
        self.geometry("820x560")
        self.config(bg="#fff8e7")
        self.resizable(False, False)

        tk.Label(self, text="Aprende sobre fracciones",
                 font=("Comic Sans MS", 20, "bold"),
                 bg="#fff8e7").pack(pady=12)

        info = ("Una fracción representa partes iguales de un todo.\n"
                "Numerador = partes tomadas. Denominador = partes totales.\n"
                "Usa los controles para dibujar fracciones y ver su representación.")
        tk.Label(self, text=info, bg="#fff8e7", font=("Arial", 12), justify="left").pack(pady=6)

        cont = tk.Frame(self, bg="#fff8e7")
        cont.pack(pady=8)

        tk.Label(cont, text="Numerador:", bg="#fff8e7").grid(row=0, column=0, padx=6)
        self.num = tk.IntVar(value=1)
        tk.Spinbox(cont, from_=0, to=20, textvariable=self.num, width=5, command=self.redibujar).grid(row=0, column=1)

        tk.Label(cont, text="Denominador:", bg="#fff8e7").grid(row=0, column=2, padx=6)
        self.den = tk.IntVar(value=4)
        tk.Spinbox(cont, from_=1, to=20, textvariable=self.den, width=5, command=self.redibujar).grid(row=0, column=3)

        self.canvas = tk.Canvas(self, width=760, height=360, bg="white", highlightthickness=1)
        self.canvas.pack(pady=12)

        self.status = tk.Label(self, text="", bg="#fff8e7", font=("Arial", 12, "bold"))
        self.status.pack()

        self.redibujar()

    def redibujar(self):
        self.canvas.delete("all")
        n = int(self.num.get())
        d = int(self.den.get())
        if d <= 0:
            self.status.config(text="Denominador debe ser mayor que 0.")
            return

        self.status.config(text=f"Fracción: {n}/{d}")

        # convert fraction to number of full circles and remainder
        completos = n // d
        sobrante = n % d

        # draw up to 4 circles per row
        max_per_row = 4
        r = 70
        padding = 30
        x_start = 40
        y_start = 60

        total = completos + (1 if sobrante > 0 else 0)
        for i in range(total):
            row = i // max_per_row
            col = i % max_per_row
            cx = x_start + col * (2*r + padding)
            cy = y_start + row * (2*r + 80)

            # base circle
            self.canvas.create_oval(cx, cy, cx + 2*r, cy + 2*r, fill="#f1f1f1", outline="#000")

            partes = d
            colorear = d if i < completos else sobrante

            # draw colored arcs
            if partes > 0:
                angle = 360 / partes
                for k in range(colorear):
                    start = 90 - (k+1)*angle
                    self.canvas.create_arc(cx, cy, cx+2*r, cy+2*r, start=start, extent=angle, fill="#ffd6a5", outline="#000")

                # draw division lines
                for k in range(partes):
                    a = math.radians(90 - k*angle)
                    x1 = cx + r + r * math.cos(a)
                    y1 = cy + r - r * math.sin(a)
                    self.canvas.create_line(cx + r, cy + r, x1, y1)

        # legend / explanation
        explanation = f"Representación de {n}/{d}. Círculos llenos: {completos}; partes coloreadas en último: {sobrante}."
        self.canvas.create_text(380, 340, text=explanation, font=("Arial", 12))

