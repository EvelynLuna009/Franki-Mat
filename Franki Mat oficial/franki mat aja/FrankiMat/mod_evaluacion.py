# modulo_evaluacion.py
import tkinter as tk
from tkinter import messagebox
import random, datetime
import math  # <- esto corrige el error math
from utils_archivos import save_backup, write_safe, read_lines_safe
from config import ARCH_RESULTADOS


class ModuloEvaluacion(tk.Toplevel):
    def __init__(self, master, alumno):
        super().__init__(master)
        self.alumno = alumno
        self.title("🧠 Evaluación - 20 preguntas mixtas")
        self.geometry("820x620")
        self.config(bg="#fff0f5")
        self.resizable(False, False)

        tk.Label(self, text=f"Evaluación - Alumno: {alumno}", font=("Comic Sans MS", 18, "bold"), bg="#fff0f5").pack(pady=10)

        # preguntas: mezcla de opción múltiple y escribir fracción
        self.preguntas = self.generar_preguntas(20)
        self.vars = []
        self.entradas = []
        self.correctos_labels = []

        container = tk.Frame(self, bg="#fff0f5")
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, bg="#fff0f5", highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.scroll_frame = tk.Frame(canvas, bg="#fff0f5")
        self.scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for i, q in enumerate(self.preguntas):
            tipo = q["tipo"]
            box = tk.LabelFrame(self.scroll_frame, text=f"Pregunta {i+1}", bg="#fff0f5", font=("Arial", 10, "bold"))
            box.pack(fill="x", padx=10, pady=6)
            tk.Label(box, text=q["texto"], bg="#fff0f5", font=("Arial", 12)).pack(anchor="w")

            if tipo == "mc":  # multiple choice
                var = tk.StringVar()
                self.vars.append(var)
                for op in q["opciones"]:
                    tk.Radiobutton(box, text=op, value=op, variable=var, bg="#fff0f5").pack(anchor="w")
                lbl = tk.Label(box, text="", bg="#fff0f5")
                lbl.pack(anchor="w")
                self.correctos_labels.append(lbl)
                self.entradas.append(None)
            else:  # escribir fracción a/b
                ent = tk.Entry(box, width=10)
                ent.pack(anchor="w", pady=6)
                self.entradas.append(ent)
                self.vars.append(None)
                lbl = tk.Label(box, text="", bg="#fff0f5")
                lbl.pack(anchor="w")
                self.correctos_labels.append(lbl)

        tk.Button(self.scroll_frame, text="Calificar", bg="#f9c5d1", width=12, command=self.calificar).pack(pady=12)
        self.result_lbl = tk.Label(self.scroll_frame, text="", bg="#fff0f5", font=("Arial", 14))
        self.result_lbl.pack(pady=6)

    # ------------------------------------------------
    # Genera preguntas mixtas
    # ------------------------------------------------
    def generar_preguntas(self, n):
        preguntas = []
        for _ in range(n):
            tipo = random.choice(["mc", "write"])
            if tipo == "mc":
                # crear pregunta sencilla de equivalencia o simplificar
                kind = random.choice(["eq","simp","mayor"])
                if kind == "eq":
                    a = random.randint(1,5); b = random.randint(2,8)
                    texto = f"¿Cuál es equivalente a {a}/{b}?"
                    correct = f"{a*2}/{b*2}"
                    opciones = [correct, f"{a}/{b+1}", f"{random.randint(1,5)}/{random.randint(2,9)}"]
                elif kind == "simp":
                    a = random.randint(2,6); b = a*2
                    texto = f"Simplifica {a*b}/{b*b} (elige la respuesta correcta)"
                    correct = f"{a}/{b}"
                    opciones = [correct, f"{(a*b)//2}/{(b*b)//2}", f"{random.randint(1,5)}/{random.randint(2,9)}"]
                else:
                    a = random.randint(1,4); b = random.randint(2,9)
                    c = random.randint(1,4); d = random.randint(2,9)
                    texto = f"¿Cuál fracción es mayor: {a}/{b} o {c}/{d}?"
                    opciones = [f"{a}/{b}", f"{c}/{d}", "Son iguales"]
                    # determine correct
                    val1 = a/b; val2 = c/d
                    if val1 == val2:
                        correct = "Son iguales"
                    elif val1 > val2:
                        correct = f"{a}/{b}"
                    else:
                        correct = f"{c}/{d}"
                preguntas.append({"tipo":"mc","texto":texto,"opciones":opciones,"correcta":correct})
            else:
                # write: suma/resta o simplificar
                kind = random.choice(["sum","simp","comp"])
                if kind == "sum":
                    a = random.randint(1,5); b = random.randint(2,9)
                    c = random.randint(1,5); d = random.randint(2,9)
                    texto = f"Resuelve: {a}/{b} + {c}/{d} (escribe en a/b simplificado)"
                    # compute correct
                    m = b*d//math.gcd(b,d)
                    n1 = a*(m//b); n2 = c*(m//d)
                    res = n1 + n2
                    g = math.gcd(res,m)
                    correcta = f"{res//g}/{m//g}"
                elif kind == "simp":
                    a = random.randint(2,8); b = a*random.randint(2,4)
                    texto = f"Simplifica: {a*b}/{b*b}"
                    num = a*b; den = b*b
                    g = math.gcd(num,den)
                    correcta = f"{num//g}/{den//g}"
                else:
                    a = random.randint(1,5); b = random.randint(2,9)
                    c = random.randint(1,5); d = random.randint(2,9)
                    texto = f"¿Cuál es mayor? Escribe '1' si la primera, '2' si la segunda, '0' si iguales: {a}/{b} vs {c}/{d}"
                    val1 = a/b; val2 = c/d
                    if val1 == val2:
                        correcta = "0"
                    elif val1 > val2:
                        correcta = "1"
                    else:
                        correcta = "2"
                preguntas.append({"tipo":"write","texto":texto,"correcta":correcta})
        return preguntas

    # ------------------------------------------------
    # Calificar y guardar resultado
    # ------------------------------------------------
    def calificar(self):
        correctas = 0
        detalles = []
        for i, q in enumerate(self.preguntas):
            if q["tipo"] == "mc":
                sel = self.vars[i].get()
                if sel == q["correcta"]:
                    correctas += 1
                    self.correctos_labels[i].config(text="✔ Correcto", fg="green")
                else:
                    self.correctos_labels[i].config(text=f"✘ Incorrecto. Correcta: {q['correcta']}", fg="red")
                    detalles.append((q["texto"], sel or "Sin responder", q["correcta"]))
            else:
                ent = self.entradas[i]
                resp = (ent.get().strip() if ent else "").strip()
                if resp == q["correcta"]:
                    correctas += 1
                    self.correctos_labels[i].config(text="✔ Correcto", fg="green")
                else:
                    self.correctos_labels[i].config(text=f"✘ Incorrecto. Correcta: {q['correcta']}", fg="red")
                    detalles.append((q["texto"], resp or "Sin responder", q["correcta"]))

        total = len(self.preguntas)
        porcentaje = int((correctas/total)*100)
        self.result_lbl.config(text=f"Puntaje: {correctas}/{total} ({porcentaje}%)")

        # Guardar en ARCH_RESULTADOS
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_backup(ARCH_RESULTADOS)
        with open(ARCH_RESULTADOS, "a", encoding="utf-8") as f:
            f.write(f"{fecha}|{self.alumno}|{correctas}/{total}|{porcentaje}%\n")
            if detalles:
                f.write("  Detalles:\n")
                for preg, tu, corr in detalles:
                    f.write(f"    - {preg}\n      Tu: {tu}\n      Correcta: {corr}\n")
            f.write("\n")

        messagebox.showinfo("Evaluación", f"Has obtenido {correctas}/{total} ({porcentaje}%)")
        # cerrar al finalizar
        self.destroy()

def ver_resultados(self):
    ventana = tk.Toplevel(self)
    ventana.title("Mis resultados")
    ventana.geometry("600x500")
    ventana.config(bg="#FFFFFF")

    tk.Label(ventana, text=f"Resultados de {self.usuario}",
             font=("Arial", 18, "bold"), bg="#FFFFFF").pack(pady=15)

    texto = tk.Text(ventana, width=70, height=20)
    texto.pack(pady=10)

    registros = [linea for linea in read_lines_safe(ARCH_RESULTADOS)
                 if linea.startswith(self.usuario + "|")]

    if registros:
        for linea in registros:
            texto.insert(tk.END, linea + "\n")
    else:
        texto.insert(tk.END, "Aún no tienes resultados guardados.")
