import tkinter as tk

class VentanaTexto(tk.Toplevel):
    def __init__(self, titulo, texto, parent):
        super().__init__(parent)

        self.title(titulo)
        self.geometry("600x500")
        self.config(bg="#ffffff")

        txt = tk.Text(self, wrap="word", font=("Arial", 12))
        txt.insert("1.0", texto)
        txt.pack(expand=True, fill="both")
