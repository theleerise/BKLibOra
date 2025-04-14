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

config_conn_lib = {
    "oracledb": "oracle+oracledb",
    "cx_oracle": "oracle+cx_oracle",
    "default_port": 1521,
    "default_host": "localhost"
}
