import tkinter as tk
from tkinter import messagebox
from utils_archivos import read_lines_safe
from config import ARCH_RESULTADOS


class VentanaAlumno(tk.Toplevel):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.title(f"Panel Alumno - {usuario}")
        self.geometry("500x500")
        self.configure(bg="#E3F2FD")
        self.resizable(False, False)

        # ---------------------------
        # Título
        # ---------------------------
        tk.Label(self, text=f"Bienvenido {usuario}", font=("Comic Sans MS", 26, "bold"),
                 bg="#E3F2FD", fg="#0D47A1").pack(pady=30)

        # ---------------------------
        # Frames
        # ---------------------------
        self.frame_principal = tk.Frame(self, bg="#E3F2FD")
        self.frame_principal.pack(pady=10)

        self.frame_practica = tk.Frame(self, bg="#E3F2FD")
        self.frame_practica.pack_forget()

        # ---------------------------
        # Botones menú principal
        # ---------------------------
        self.btn_aprendizaje = tk.Button(self.frame_principal, text="📘 Aprendizaje",
                                         font=("Arial", 14), width=35, bg="#90CAF9",
                                         command=self.abrir_aprendizaje)
        self.btn_aprendizaje.pack(pady=10)

        self.btn_practica_main = tk.Button(self.frame_principal, text="📗 Práctica / Ejercicios",
                                           font=("Arial", 14), width=35, bg="#A5D6A7",
                                           command=self.mostrar_practica)
        self.btn_practica_main.pack(pady=10)

        self.btn_evaluacion = tk.Button(self.frame_principal, text="📕 Evaluación",
                                        font=("Arial", 14), width=35, bg="#F48FB1",
                                        command=self.abrir_evaluacion)
        self.btn_evaluacion.pack(pady=10)

        self.btn_resultados = tk.Button(self.frame_principal, text="📊 Ver mis resultados",
                                        font=("Arial", 14), width=35, bg="#DCE775",
                                        command=self.ver_resultados)
        self.btn_resultados.pack(pady=10)

        self.btn_regresar = tk.Button(self.frame_principal, text="🔙 Regresar",
                                      font=("Arial", 14), width=20, bg="#FFF59D",
                                      command=self.regresar)
        self.btn_regresar.pack(pady=10)

        self.btn_cerrar = tk.Button(self.frame_principal, text="❌ Cerrar sesión",
                                    font=("Arial", 14), width=20, bg="#EF9A9A",
                                    command=self.cerrar_sesion)
        self.btn_cerrar.pack(pady=10)

        # ---------------------------
        # Botones submenú práctica
        # ---------------------------
        self.btn_practica = tk.Button(self.frame_practica, text="Práctica",
                                      font=("Arial", 14), width=35, bg="#B3E5FC",
                                      command=self.abrir_ventana_practica)
        self.btn_practica.pack(pady=10)

        self.btn_comparacion = tk.Button(self.frame_practica, text="Comparación de fracciones",
                                         font=("Arial", 14), width=35, bg="#FFE082",
                                         command=self.abrir_ventana_comparacion)
        self.btn_comparacion.pack(pady=10)

        self.btn_ejercicios = tk.Button(self.frame_practica, text="Ejercicios",
                                        font=("Arial", 14), width=35, bg="#B2DFDB",
                                        command=self.abrir_ventana_ejercicios)
        self.btn_ejercicios.pack(pady=10)

        self.btn_regresar_practica = tk.Button(self.frame_practica, text="🔙 Regresar",
                                               font=("Arial", 14), width=20, bg="#FFF59D",
                                               command=self.volver_menu)
        self.btn_regresar_practica.pack(pady=10)

        self.btn_cerrar_practica = tk.Button(self.frame_practica, text="❌ Cerrar sesión",
                                             font=("Arial", 14), width=20, bg="#EF9A9A",
                                             command=self.cerrar_sesion)
        self.btn_cerrar_practica.pack(pady=10)

    # ---------------------------
    # Funciones de navegación
    # ---------------------------
    def mostrar_practica(self):
        self.frame_principal.pack_forget()
        self.frame_practica.pack(pady=10)

    def volver_menu(self):
        self.frame_practica.pack_forget()
        self.frame_principal.pack(pady=10)

    # ---------------------------
    # Funciones de botones
    # ---------------------------
    def abrir_aprendizaje(self):
        try:
            import ventana_aprendizaje
            ventana_aprendizaje.VentanaAprendizaje(self.usuario)
        except ModuleNotFoundError:
            messagebox.showinfo("Aprendizaje", "Módulo Aprendizaje no disponible aún.")

    def abrir_ventana_practica(self):
        try:
            import ventana_practica
            ventana_practica.VentanaPractica(self.usuario)
        except ModuleNotFoundError:
            messagebox.showinfo("Práctica", "Módulo de práctica no disponible aún.")

    def abrir_ventana_ejercicios(self):
        try:
            import ventana_ejercicios
            ventana_ejercicios.VentanaEjercicios(self.usuario)
        except ModuleNotFoundError:
            messagebox.showinfo("Ejercicios", "Módulo de ejercicios no disponible aún.")

    def abrir_ventana_comparacion(self):
        try:
            import ventana_comparacion
            ventana_comparacion.VentanaComparacion(self.usuario)
        except ModuleNotFoundError:
            messagebox.showinfo("Comparación", "Módulo de comparación no disponible aún.")

    def abrir_evaluacion(self):
        """★ Aquí está la función ya corregida y funcionando ★"""
        try:
            import ventana_evaluacion
            ventana_evaluacion.VentanaEvaluacion(self.usuario)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el módulo Evaluación:\n{e}")

    # ---------------------------
    # Ver resultados
    # ---------------------------
    def ver_resultados(self):
        ventana = tk.Toplevel(self)
        ventana.title("Mis resultados")
        ventana.geometry("600x500")
        ventana.config(bg="#FFFFFF")

        tk.Label(ventana, text=f"Resultados de {self.usuario}",
                 font=("Arial", 18, "bold"), bg="#FFFFFF").pack(pady=15)

        texto = tk.Text(ventana, width=70, height=20)
        texto.pack(pady=10)

        registros = [
            linea for linea in read_lines_safe(ARCH_RESULTADOS)
            if f"|{self.usuario}|" in linea
        ]

        if registros:
            for linea in registros:
                texto.insert(tk.END, linea + "\n")
        else:
            texto.insert(tk.END, "Aún no tienes resultados guardados.")

    # ---------------------------
    # Regresar / Cerrar sesión
    # ---------------------------
    def regresar(self):
        self.destroy()

    def cerrar_sesion(self):
        messagebox.showinfo("Sesión cerrada", "La sesión ha sido cerrada.")
        self.destroy()
