"""
Módulo de configuración de conexión Oracle (`config.py`)
--------------------------------------------------------

Este módulo define un diccionario centralizado con la configuración por defecto para establecer conexiones con bases de datos Oracle,
utilizado por la librería `BKLibOra`.

El diccionario `config_conn_lib` proporciona:

- Dialectos compatibles con SQLAlchemy para los drivers `oracledb` y `cx_Oracle`.
- Parámetros por defecto para el host y puerto.

Atributos:
    config_conn_lib (dict): Diccionario de configuración de conexión.
        Claves:
            - "oracledb" (str): Dialecto SQLAlchemy para el driver `oracledb`.
            - "cx_oracle" (str): Dialecto SQLAlchemy para el driver `cx_Oracle`.
            - "default_port" (int): Puerto por defecto del servicio Oracle.
            - "default_host" (str): Host por defecto (normalmente `localhost`).
"""
import cx_Oracle

config_conn_lib = {
    "oracledb": "oracle+oracledb",
    "cx_oracle": "oracle+cx_oracle",
    "default_port": 1521,
    "default_host": "localhost"
}

roles_base = {
    "SYSDBA" : cx_Oracle.SYSDBA,
    "SYSOPER" : cx_Oracle.SYSOPER,
    "SYSASM" : cx_Oracle.SYSASM,
    "SYSBKP" : cx_Oracle.SYSBKP,
    "SYSDGD" : cx_Oracle.SYSDGD,
    "SYSKMT" : cx_Oracle.SYSKMT,
    "SYSRAC" : cx_Oracle.SYSRAC,
    "DEFAULT" : cx_Oracle.DEFAULT_AUTH,  
}

MAX_VALUES = {
    "string": 4000,  # Máximo de caracteres para cadenas
    "number": 38,    # Máximo de dígitos para números
    "date": None,    # No hay límite específico para fechas
    "timestamp": None,  # No hay límite específico para timestamps
    "clob": None,    # CLOB puede ser muy grande, sin límite específico
    "blob": None     # BLOB puede ser muy grande, sin límite específico
}