import tkinter as tk
from tkinter import messagebox
from usuarios import cargar_usuarios, guardar_usuario
from seguridad import verify_password
from config import ARCH_MAESTROS, ARCH_ALUMNOS
import re


# ------------------------------
# Validación de contraseña
# ------------------------------
def validar_password(password):
    """
    Requisitos:
    - mínimo 8 caracteres
    - al menos 1 letra
    """
    if len(password) < 8:
        return False
    if not re.search(r"[A-Za-z]", password):
        return False
    return True


# --------------------------------------------------
# Ventana principal: Selección Maestro / Alumno
# --------------------------------------------------
class VentanaLogin(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("FRANKI MAT - Inicio de sesión")
        self.geometry("450x420")
        self.config(bg="#dff6ff")
        self.resizable(False, False)

        tk.Label(
            self,
            text="FRANKI MAT",
            font=("Comic Sans MS", 32, "bold"),
            bg="#dff6ff",
            fg="#053B50"
        ).pack(pady=30)

        tk.Button(
            self,
            text="👩‍🏫 Maestro",
            font=("Arial", 14),
            bg="#a2d2ff",
            width=20,
            command=self.abrir_login_maestro
        ).pack(pady=15)

        tk.Button(
            self,
            text="👨‍🎓 Alumno",
            font=("Arial", 14),
            bg="#bde0fe",
            width=20,
            command=self.abrir_login_alumno
        ).pack(pady=15)

        tk.Button(
            self,
            text="Salir",
            bg="#ff9b9b",
            width=15,
            command=self.destroy
        ).pack(pady=25)

    def abrir_login_maestro(self):
        LoginUsuario(self, "maestro")

    def abrir_login_alumno(self):
        LoginUsuario(self, "alumno")


# --------------------------------------------------
# Ventana interna: Login y registro
# --------------------------------------------------
class LoginUsuario(tk.Toplevel):
    def __init__(self, master, tipo):
        super().__init__(master)

        self.tipo = tipo
        self.title(f"Inicio de sesión - {tipo.capitalize()}")
        self.geometry("480x450")
        self.config(bg="#f0f7ff")
        self.resizable(False, False)

        self.archivo = ARCH_MAESTROS if tipo == "maestro" else ARCH_ALUMNOS

        tk.Label(
            self,
            text=f"{tipo.capitalize()} - Login / Registro",
            font=("Comic Sans MS", 20, "bold"),
            bg="#f0f7ff"
        ).pack(pady=20)

        frame = tk.Frame(self, bg="#f0f7ff")
        frame.pack()

        tk.Label(frame, text="Usuario:", bg="#f0f7ff").grid(row=0, column=0, padx=10, pady=10)
        self.e_user = tk.Entry(frame, width=28)
        self.e_user.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(frame, text="Contraseña:", bg="#f0f7ff").grid(row=1, column=0, padx=10, pady=10)

        # -------------------------
        # CAMPO CONTRASEÑA + BOTÓN
        # -------------------------
        self.e_pwd = tk.Entry(frame, width=28, show="*")
        self.e_pwd.grid(row=1, column=1, padx=10, pady=10)

        self.ver_pwd = False
        self.btn_ver = tk.Button(
            frame,
            text="👁",
            command=self.toggle_password,
            width=3
        )
        self.btn_ver.grid(row=1, column=2)

        # BOTONES
        tk.Button(
            self,
            text="Iniciar sesión",
            bg="#a2d2ff",
            width=20,
            command=self.iniciar
        ).pack(pady=12)

        tk.Button(
            self,
            text="Registrarse",
            bg="#bde0fe",
            width=20,
            command=self.registrar
        ).pack()

    # ------------------------------------------
    # Mostrar / ocultar contraseña
    # ------------------------------------------
    def toggle_password(self):
        self.ver_pwd = not self.ver_pwd
        self.e_pwd.config(show="" if self.ver_pwd else "*")
        self.btn_ver.config(text="🚫" if self.ver_pwd else "👁")

    # ------------------------------------------
    # Iniciar sesión
    # ------------------------------------------
    def iniciar(self):
        user = self.e_user.get().strip()
        pwd = self.e_pwd.get().strip()

        if not user or not pwd:
            messagebox.showwarning("Campos vacíos", "Debe ingresar usuario y contraseña.")
            return

        usuarios = cargar_usuarios(self.archivo)

        if user not in usuarios:
            messagebox.showerror("Error", "El usuario no existe.")
            return

        stored_hash = usuarios[user]

        if verify_password(stored_hash, pwd):

            # Cerrar login y abrir panel sin mostrar mensaje
            self.destroy()

            if self.tipo == "maestro":
                from ventana_maestro import VentanaMaestro
                VentanaMaestro(user)
            else:
                from ventana_alumno import VentanaAlumno
                VentanaAlumno(user)

        else:
            messagebox.showerror("Error", "Contraseña incorrecta.")

    # ------------------------------------------
    # Registrar usuario
    # ------------------------------------------
    def registrar(self):
        user = self.e_user.get().strip()
        pwd = self.e_pwd.get().strip()

        if not user or not pwd:
            messagebox.showwarning("Campos vacíos", "Debe ingresar usuario y contraseña.")
            return

        if not validar_password(pwd):
            messagebox.showwarning(
                "Contraseña insegura",
                "La contraseña debe tener:\n\n- mínimo 8 caracteres\n- al menos 1 letra"
            )
            return

        usuarios = cargar_usuarios(self.archivo)
        if user in usuarios:
            messagebox.showwarning("Duplicado", "El usuario ya existe.")
            return

        guardar_usuario(self.archivo, user, pwd)

        messagebox.showinfo(
            "Registro exitoso",
            "Usuario creado correctamente.\nAhora puedes iniciar sesión."
        )
