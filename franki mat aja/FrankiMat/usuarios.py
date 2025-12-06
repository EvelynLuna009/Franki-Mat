# usuarios.py
from utils_archivos import write_safe, read_lines_safe, save_backup
from seguridad import hash_password, verify_password

# ---------------------------
# Validaciones
# ---------------------------

def validar_nombre(nombre):
    return nombre.isalnum() and len(nombre) >= 4

def validar_password(password):
    # Mínimo 8 caracteres y mínimo 1 letra
    if len(password) < 8:
        return False
    if not any(c.isalpha() for c in password):
        return False
    return True

# ---------------------------
# Cargar usuarios
# ---------------------------

def cargar_usuarios(path):
    usuarios = {}
    for linea in read_lines_safe(path):
        if not linea.strip():
            continue
        partes = linea.split("|")
        if len(partes) >= 2:
            usuario, stored_hash = partes[0], partes[1]
            usuarios[usuario] = stored_hash
    return usuarios

# ---------------------------
# Guardar usuario (registrar)
# ---------------------------

def guardar_usuario(path, usuario, password):
    pwd_hash = hash_password(password)
    save_backup(path)
    write_safe(path, f"{usuario}|{pwd_hash}\n")
    return True

# ---------------------------
# Registrar con validaciones
# ---------------------------

def registrar_usuario(path, usuario, password):
    if not validar_nombre(usuario):
        return "nombre_invalido"

    if not validar_password(password):
        return "password_invalido"

    usuarios = cargar_usuarios(path)
    if usuario in usuarios:
        return "existe"

    guardar_usuario(path, usuario, password)
    return "ok"
