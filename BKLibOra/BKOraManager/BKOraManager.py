"""
Módulo BKOraManager
-------------------

Este módulo define la clase `BKOraManager`, una interfaz de alto nivel para ejecutar consultas sobre una base de datos Oracle
utilizando SQLAlchemy, gestionando automáticamente el ciclo de vida de las sesiones con un contexto seguro.

Clases:
    BKOraManager

Dependencias:
    - contextlib
    - sqlalchemy (a través del conector proporcionado)
"""

from sqlalchemy.sql import text
from contextlib import contextmanager


class BKOraManager:
    """
    Gestor de operaciones SQL sobre una base de datos Oracle usando SQLAlchemy.

    Esta clase proporciona métodos de utilidad para ejecutar consultas SQL (SELECT, DML) dentro de un
    contexto de sesión controlado que garantiza commit, rollback y cierre seguro.

    Args:
        connector (BKOraConnect): Instancia del conector `BKOraConnect` que expone el método `get_session()`.

    Métodos:
        session_scope(): Context manager que maneja la apertura, commit, rollback y cierre de la sesión.
        fetch_all(query, params=None): Ejecuta una consulta y devuelve todos los resultados como lista de diccionarios.
        fetch_one(query, params=None): Ejecuta una consulta y devuelve un único resultado como diccionario.
        execute(query, params=None): Ejecuta una instrucción SQL sin retornar resultados (ideal para INSERT, UPDATE, DELETE).
    """

    def __init__(self, connector):
        """
        Inicializa una instancia de BKOraManager.

        Args:
            connector (BKOraConnect): Conector a la base de datos.
        """
        self.connector = connector

    @contextmanager
    def session_scope(self):
        """
        Context manager que proporciona un ámbito de sesión seguro.

        Abre una sesión, realiza commit si todo va bien o rollback en caso de excepción, y finalmente cierra la sesión.

        Yields:
            sqlalchemy.orm.Session: Objeto sesión activo.
        """
        session = self.connector.get_session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def fetch_all(self, query, params=None):
        """
        Ejecuta una consulta SQL y devuelve todos los resultados.

        Args:
            query (str): Consulta SQL (de tipo SELECT).
            params (dict, optional): Parámetros para la consulta.

        Returns:
            list[dict]: Lista de filas como diccionarios (clave=nombre de columna).
        """
        with self.session_scope() as session:
            result = session.execute(text(query), params or {})
            keys = result.keys()
            return [dict(zip(keys, row)) for row in result]

    def fetch_one(self, query, params=None):
        """
        Ejecuta una consulta SQL y devuelve una única fila como diccionario.

        Args:
            query (str): Consulta SQL (de tipo SELECT).
            params (dict, optional): Parámetros para la consulta.

        Returns:
            dict | None: Fila como diccionario o None si no hay resultados.
        """
        with self.session_scope() as session:
            result = session.execute(text(query), params or {})
            row = result.fetchone()
            if row:
                return dict(zip(result.keys(), row))
            return None

    def execute(self, query, params=None):
        """
        Ejecuta una consulta SQL sin devolver resultados (ideal para INSERT, UPDATE, DELETE).

        Args:
            query (str): Consulta SQL.
            params (dict, optional): Parámetros de la consulta.
        """
        with self.session_scope() as session:
            session.execute(text(query), params or {})
