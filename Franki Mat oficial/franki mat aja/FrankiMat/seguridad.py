# seguridad.py
# ------------------------------------------------------------
# Módulo de seguridad para FRANKI MAT
# Manejo de contraseñas seguras con SHA256 + SALT aleatorio
# ------------------------------------------------------------

import os
import hashlib

# ------------------------------------------------------------
# GENERAR SALT
# ------------------------------------------------------------
def generar_salt(longitud=16):
    """
    Genera un SALT aleatorio en formato hexadecimal.
    Longitud por defecto: 16 bytes → 32 caracteres hex.
    """
    return os.urandom(longitud).hex()

# ------------------------------------------------------------
# HASHEAR CONTRASEÑA
# ------------------------------------------------------------
def hash_password(password):
    """
    Genera un hash seguro en formato:
        salt$hash

    Donde:
    - salt es un valor aleatorio único
    - hash es SHA256(salt + password)
    """
    salt = generar_salt()
    hash_hex = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}${hash_hex}"

# ------------------------------------------------------------
# VERIFICAR CONTRASEÑA
# ------------------------------------------------------------
def verify_password(stored_value, password):
    """
    Verifica una contraseña con el formato salt$hash.

    Retorna:
        True  → si la contraseña coincide
        False → si es incorrecta o el formato no es válido
    """
    try:
        salt, stored_hash = stored_value.split("$")
    except ValueError:
        # Si el stored_value no tiene el formato correcto
        return False

    # Rehash usando el SALT guardado
    new_hash = hashlib.sha256((salt + password).encode()).hexdigest()

    return stored_hash == new_hash

# ------------------------------------------------------------
# UTILIDAD: ¿EL FORMATO ES VÁLIDO?
# ------------------------------------------------------------
def formato_hash_valido(texto):
    """
    Verifica si un texto tiene formato SALT$HASH.
    Útil para evitar errores al cargar usuarios.
    """
    return "$" in texto and len(texto.split("$")) == 2
