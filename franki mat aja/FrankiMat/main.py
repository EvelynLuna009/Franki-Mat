# -----------------------------------------------------------
# MAIN.PY — PROGRAMA PRINCIPAL FRANKI MAT
# -----------------------------------------------------------

import tkinter as tk
from ventanas_login import VentanaLogin
from utils_archivos import asegurar_estructura


def main():
    # Crear ventana raíz invisible
    root = tk.Tk()
    root.withdraw()

    # Crear carpetas y archivos si no existen
    asegurar_estructura()

    # Abrir ventana principal de inicio de sesión
    VentanaLogin(root)

    # Mantener ejecución
    root.mainloop()


if __name__ == "__main__": 
    main()
