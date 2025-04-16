"""
Módulo BKOraConnect
-------------------

Este módulo proporciona la clase `BKOraConnect`, diseñada para facilitar la conexión a bases de datos Oracle mediante SQLAlchemy.
Es compatible con los drivers `cx_Oracle` y `oracledb`, permitiendo crear sesiones ORM y administrar la conexión de forma flexible.

Requiere un archivo de configuración con los valores por defecto y los dialectos para cada driver en `BKLibOra.config.config_conn_lib`.

Clases:
    BKOraConnect

Dependencias:
    - sqlalchemy
    - cx_Oracle
    - oracledb (opcional, si se usa el modo thick)
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import cx_Oracle

from BKLibOra.config import config_conn_lib as conn, roles_base as rol


class BKOraConnect:
    """
    Clase de conexión para bases de datos Oracle utilizando SQLAlchemy.

    Soporta conexión usando Service Name, SID o TNS Alias, y permite seleccionar entre los drivers `cx_Oracle` y `oracledb`.

    Args:
        user (str): Usuario de la base de datos.
        password (str): Contraseña del usuario.
        host (str, optional): Dirección del host de la base de datos. Por defecto, el valor definido en `config_conn_lib["default_host"]`.
        port (int, optional): Puerto del servicio Oracle. Por defecto, el valor definido en `config_conn_lib["default_port"]`.
        service_name (str, optional): Nombre del servicio Oracle (SERVICE_NAME).
        sid (str, optional): Identificador del sistema Oracle (SID).
        tns_alias (str, optional): Alias TNS definido en `tnsnames.ora`.
        use_thick (bool, optional): Si es `True`, se inicializa el cliente Oracle en modo "thick" (requiere Oracle Instant Client).

    Raises:
        ValueError: Si no se proporciona ninguno de los parámetros `service_name`, `sid` o `tns_alias`.

    Atributos:
        engine (sqlalchemy.Engine): Motor de conexión SQLAlchemy.
        Session (sqlalchemy.orm.session.sessionmaker): Fábrica de sesiones SQLAlchemy.
    """

    def __init__(self, user, password, host=conn.get("default_host"), port=conn.get("default_port"),
                 service_name=None, sid=None, tns_alias=None, use_thick=False, role_mode="DEFAULT"):
        connection_args = {}
        
        if use_thick:
            import oracledb
            oracledb.init_oracle_client()
            dialect = conn.get("oracledb")
        else:
            dialect = conn.get("cx_oracle")

        if tns_alias:
            dsn = tns_alias
        elif service_name:
            dsn = cx_Oracle.makedsn(host, port, service_name=service_name)
        elif sid:
            dsn = cx_Oracle.makedsn(host, port, sid=sid)
        else:
            raise ValueError("Debes proporcionar al menos service_name, sid o tns_alias")
        
        if role_mode is not None:
            connection_args["mode"] = rol.get(role_mode)

        connection_url = f"{dialect}://{user}:{password}@{dsn}"
        self.engine = create_engine(connection_url, connect_args=connection_args, pool_pre_ping=True)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        """
        Crea una nueva sesión SQLAlchemy enlazada al motor de conexión.

        Returns:
            sqlalchemy.orm.Session: Sesión activa para operaciones ORM.
        """
        return self.Session()

    def dispose(self):
        """
        Libera los recursos del motor de SQLAlchemy cerrando el pool de conexiones.
        """
        self.engine.dispose()

        
# # Usando service_name
# conn = BKOraConnect(user="scott", password="tiger", host="localhost", service_name="orcl")
# 
# # Usando SID
# conn = BKOraConnect(user="scott", password="tiger", host="localhost", sid="ORCL")
# 
# # Usando alias TNS
# conn = BKOraConnect(user="scott", password="tiger", tns_alias="MI_ALIAS")
# 
# # Usando oracledb en modo thick
# conn = BKOraConnect(user="scott", password="tiger", host="localhost", service_name="orcl", use_thick=True)
