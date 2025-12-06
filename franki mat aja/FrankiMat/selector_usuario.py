import tkinter as tk
from ventanas_login import VentanaLogin

class SelectorUsuario(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FRANKI MAT - Seleccionar Usuario")
        self.geometry("350x240")
        self.resizable(False, False)
        self.config(bg="#e3f2fd")

        tk.Label(self, text="FRANKI MAT", font=("Comic Sans MS", 26, "bold"),
                 bg="#e3f2fd").pack(pady=20)

        tk.Button(self, text="Soy Maestro", width=18, height=2, bg="#bde0fe",
                  command=lambda: VentanaLogin(self, "maestro")).pack(pady=8)

        tk.Button(self, text="Soy Alumno", width=18, height=2, bg="#caffbf",
                  command=lambda: VentanaLogin(self, "alumno")).pack(pady=5)

if __name__ == "__main__":
    SelectorUsuario().mainloop()
