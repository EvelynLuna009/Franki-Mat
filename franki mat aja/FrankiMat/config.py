# -----------------------------------------------------------
# CONFIGURACIÓN GENERAL
# -----------------------------------------------------------

import os

CARPETA_DATOS = "datos"
USERS_DIR = os.path.join(CARPETA_DATOS, "usuarios")

# Archivos de usuarios
ARCH_MAESTROS = os.path.join(USERS_DIR, "maestros.txt")
ARCH_ALUMNOS = os.path.join(USERS_DIR, "alumnos.txt")

# Otros archivos
ARCH_RESULTADOS = os.path.join(CARPETA_DATOS, "resultados_alumnos.txt")
AUDIT_LOG = os.path.join(CARPETA_DATOS, "auditoria.log")
BACKUP_DIR = os.path.join(CARPETA_DATOS, "backups")

# Seguridad
MAX_INTENTOS = 3
BLOQUEO_SEGUNDOS = 300  # 5 minutos

