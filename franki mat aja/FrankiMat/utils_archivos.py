import os, shutil, datetime
from config import *

def asegurar_estructura():
    os.makedirs(CARPETA_DATOS, exist_ok=True)
    os.makedirs(USERS_DIR, exist_ok=True)
    os.makedirs(BACKUP_DIR, exist_ok=True)

    for ruta in (ARCH_MAESTROS, ARCH_ALUMNOS, ARCH_RESULTADOS, AUDIT_LOG):
        if not os.path.exists(ruta):
            with open(ruta, "w", encoding="utf-8") as f:
                f.write("")

def write_safe(path, text):
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(text)
    except Exception:
        pass

def read_lines_safe(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return [l.rstrip("\n") for l in f.readlines()]
    except:
        return []

def save_backup(path):
    if os.path.exists(path):
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        dest = os.path.join(BACKUP_DIR, os.path.basename(path) + "_" + ts + ".bak")
        shutil.copy(path, dest)

def log_event(user, accion):
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(f"{fecha} | {user} | {accion}\n")