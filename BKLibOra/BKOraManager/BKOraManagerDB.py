"""
Módulo BKOraManagerDB
---------------------

Este módulo define la clase abstracta `BKOraManagerDB`, una extensión de `BKOraManager` orientada a manejar operaciones
CRUD (Create, Read, Update, Delete) sobre modelos personalizados, así como la ejecución de procedimientos y funciones almacenadas.

La clase espera que el modelo proporcionado tenga:
- un método `to_dict()` para convertir instancias del modelo en diccionarios (clave: nombre de columna, valor: valor).
- un método `from_list()` para transformar una lista de diccionarios en una lista de objetos del modelo.

Clases:
    BKOraManagerDB

Dependencias:
    - BKOraManager (de BKLibOra)
    - abc (para clases abstractas)

Resumen de métodos:
    - getlist(): Ejecuta una consulta SELECT definida por la subclase y devuelve una lista de objetos del modelo.
    - insert_model(objmodel): Inserta un objeto en la base de datos, usando los hooks before/after_insert.
    - update_model(objmodel): Actualiza un objeto en la base de datos, usando los hooks before/after_update.
    - delete_model(objmodel): Elimina un objeto en la base de datos, usando los hooks before/after_delete.
    - call_procedure(proc_name, params): Ejecuta un procedimiento almacenado.
    - call_function(func_name, params): Ejecuta una función almacenada y devuelve su valor.

Hooks personalizables (opcionalmente sobreescribibles):
    - before_insert / after_insert
    - before_update / after_update
    - before_delete / after_delete

Métodos abstractos que deben ser implementados por la subclase:
    - get_sql_select()
    - get_sql_insert()
    - get_sql_update()
    - get_sql_delete()
"""

from BKLibOra.BKOraManager.BKOraManager import BKOraManager
from BKLibOra.BKOraManager.BKOraManager_utils import counter_row_query, range_row_query
from sqlalchemy.orm import sessionmaker
from abc import ABC, abstractmethod
import time


class BKOraManagerDB(BKOraManager):
    """
    Clase base abstracta para manejar operaciones CRUD sobre una tabla Oracle usando un modelo.

    Esta clase delega la ejecución SQL a `BKOraManager` y delega la definición de sentencias SQL
    al desarrollador que herede esta clase, a través de métodos abstractos.

    Args:
        connector (BKOraConnect): Conector a la base de datos.
        model (object): Clase modelo con métodos `to_dict()` y `from_list()`.
        args (list)
        kwargs (dict)

    Métodos abstractos:
        get_sql_select(): Devuelve la sentencia SELECT y parámetros asociados.
        get_sql_insert(): Devuelve la sentencia INSERT y parámetros asociados.
        get_sql_update(): Devuelve la sentencia UPDATE y parámetros asociados.
        get_sql_delete(): Devuelve la sentencia DELETE y parámetros asociados.

    Métodos sobrescribibles:
        before_insert(params): Lógica previa a la ejecución de un INSERT.
        after_insert(params): Lógica posterior a la ejecución de un INSERT.
        before_update(params): Lógica previa a la ejecución de un UPDATE.
        after_update(params): Lógica posterior a la ejecución de un UPDATE.
        before_delete(params): Lógica previa a la ejecución de un DELETE.
        after_delete(params): Lógica posterior a la ejecución de un DELETE.
    """
    DEFAULT_KWARGS = {
        "rows_page": 20,
        "row_page_tab" : 5
    }

    def __init__(self, connector, model, *args, **kwargs):
        """
        Inicializa una instancia de BKOraManagerDB.

        Args:
            connector (BKOraConnect): Conector con método `get_session()`.
            model (object): Clase modelo con `to_dict()` y `from_list()`.
        """
        super().__init__(connector=connector)
        self.model = model
        self.args = args
        self.kwargs = self.DEFAULT_KWARGS | kwargs

    @abstractmethod
    def get_sql_select(self):
        """
        Devuelve la sentencia SELECT y los parámetros asociados.

        Returns:
            tuple[str, dict]: Consulta SQL y parámetros.
        """
        pass

    @abstractmethod
    def get_sql_insert(self):
        """
        Devuelve la sentencia INSERT y los parámetros asociados.

        Returns:
            tuple[str, dict]: Consulta SQL y parámetros.
        """
        pass

    @abstractmethod
    def get_sql_update(self):
        """
        Devuelve la sentencia UPDATE y los parámetros asociados.

        Returns:
            tuple[str, dict]: Consulta SQL y parámetros.
        """
        pass

    @abstractmethod
    def get_sql_delete(self):
        """
        Devuelve la sentencia DELETE y los parámetros asociados.

        Returns:
            tuple[str, dict]: Consulta SQL y parámetros.
        """
        pass

    def getlist(self, session: sessionmaker|None=None) -> dict:
        """
        Ejecuta la consulta SELECT definida por `get_sql_select()` y convierte los resultados a modelos.

        Returns:
            list[object]: Lista de instancias del modelo definido.
        """
        sql, params = self.get_sql_select()
        results = self.fetch_all(sql, params, sess=session)
        return self.model.from_list(results)
    
    def getlist_numerated(self, session: sessionmaker|None=None) -> dict:
        """
        Devuelve todos los registros que cumple la consulta, el total de filas
        y métricas de tiempo de ejecución.

        El método ejecuta la sentencia SQL generada por ``get_sql_select()``,
        transforma el resultado crudo en instancias del modelo mediante
        ``self.model.from_list`` y calcula:

        * ``count``: número total de filas que devuelve la consulta.
        * ``time_result``: tiempo en obtener y mapear los resultados.
        * ``time_count``: tiempo en calcular el total de filas.
        * ``time_exec``: tiempo total del método.

        Args:
            session (sessionmaker | None, opcional):
                Sesión de SQLAlchemy a reutilizar.  
                Si ``None`` se usa la configuración por defecto
                interna de ``fetch_all``.

        Returns:
            dict:  
                Diccionario con las claves:

                * ``result`` (list[Model]): lista de instancias del modelo.
                * ``result_set`` (Sequence[RowMapping]): datos crudos devueltos
                  por el driver SQL.
                * ``count`` (int): total de registros.
                * ``time`` (dict): métricas de rendimiento descritas arriba.

        See Also:
            * :py:meth:`get_sql_select`
            * :py:meth:`fetch_all`
            * :py:meth:`model.from_list`
        """

        time_exec_init = time.perf_counter()

        sql, params = self.get_sql_select()
        counter_query = counter_row_query(sql)

        time_count_init = time.perf_counter()
        count = self.fetch_all(counter_query, params, sess=session)
        time_count = time.perf_counter() - time_count_init

        time_result_init = time.perf_counter()
        result_set = self.fetch_all(sql, params, sess=session)
        result_models = self.model.from_list(result_set)
        time_result = time.perf_counter() - time_result_init

        time_exec = time.perf_counter() - time_exec_init

        result_dict = {
            "result": result_models,
            "result_set": result_set,
            "count": count,
            "time": {
                "time_result": time_result,
                "time_count": time_count,
                "time_exec": time_exec,
            }
        }

        return result_dict

    def getlist_paginated(self, session: sessionmaker|None=None) -> dict:
        """
        Obtiene todos los registros pero los divide en páginas de tamaño fijo.

        El tamaño de página se lee de ``self.kwargs["rows_page"]``.  El flujo
        de trabajo es idéntico a :py:meth:`getlist_numerated` con la diferencia
        de que los resultados se dividen en chunks:

        .. code-block:: python

            chunks = [
                result_models[i : i + rows_page]
                for i in range(0, len(result_models), rows_page)
            ]

        Args:
            session (sessionmaker | None, opcional):
                Sesión de SQLAlchemy a reutilizar.

        Returns:
            dict:  
                * ``result`` (list[list[Model]]): lista de páginas; cada página
                  es una lista de instancias del modelo.
                * ``result_set`` (Sequence[RowMapping])
                * ``count`` (int)
                * ``time`` (dict): incluye además ``time_page`` con el tiempo
                  empleado en paginar.

        Raises:
            KeyError: si ``"rows_page"`` no está presente en ``self.kwargs``.
        """

        time_exec_init = time.perf_counter()

        sql, params = self.get_sql_select()
        counter_query = counter_row_query(sql)

        time_count_init = time.perf_counter()
        count = self.fetch_all(counter_query, params, sess=session)
        time_count = time.perf_counter() - time_count_init

        time_result_init = time.perf_counter()
        result_set = self.fetch_all(sql, params, sess=session)
        result_models = self.model.from_list(result_set)
        time_result = time.perf_counter() - time_result_init

        time_page_init = time.perf_counter()
        chunks = [result_models[i:i + self.kwargs.get("rows_page")]
                  for i in range(0, len(result_models), self.kwargs.get("rows_page"))]
        time_page = time.perf_counter() - time_page_init

        time_exec = time.perf_counter() - time_exec_init

        result_dict = {
            "result": chunks,
            "result_set": result_set,
            "count": count,
            "time": {
                "time_page": time_page,
                "time_result": time_result,
                "time_count": time_count,
                "time_exec": time_exec,
            }
        }

        return result_dict
    
    def getlist_page(self, page_range: dict|None=None, session: sessionmaker|None=None) -> dict:
        """
        Devuelve solo la página solicitada mediante límites ``OFFSET``/``LIMIT``.

        El rango por defecto selecciona desde la fila 0 hasta
        ``self.kwargs["rows_page"]`` (excluido el límite).

        Args:
            page_range (dict | None, opcional):
                Diccionario con las claves:

                * ``page_init`` (int): índice inicial —‐corresponde a *OFFSET*.
                * ``page_fin`` (int): número de filas a devolver —‐corresponde a
                  *LIMIT*.

                Si es ``None`` se utiliza el rango por defecto indicado arriba.
            session (sessionmaker | None, opcional):
                Sesión de SQLAlchemy a reutilizar.

        Returns:
            dict: estructura análoga a :py:meth:`getlist_numerated`.

        Nota:
            El contador ``count`` se calcula **contra la sub-consulta paginada**,
            no contra la consulta original sin límites.
        """

        time_exec_init = time.perf_counter()

        if not page_range:
            page_range = {
                "page_init": 0,
                "page_fin": self.kwargs.get("rows_page"),
            }

        sql, params = self.get_sql_select()
        sql = range_row_query(sql, offset=page_range.get("page_init"), limit=page_range.get("page_fin"))
        counter_query = counter_row_query(sql)

        time_count_init = time.perf_counter()
        count = self.fetch_all(counter_query, params, sess=session)
        time_count = time.perf_counter() - time_count_init

        time_result_init = time.perf_counter()
        result_set = self.fetch_all(sql, params, sess=session)
        result_models = self.model.from_list(result_set)
        time_result = time.perf_counter() - time_result_init

        time_exec = time.perf_counter() - time_exec_init

        result_dict = {
            "result": result_models,
            "result_set": result_set,
            "count": count,
            "time": {
                "time_result": time_result,
                "time_count": time_count,
                "time_exec": time_exec,
            }
        }

        return result_dict

    def getlist_range(self, _range: tuple|None=None, session: sessionmaker|None=None):
        """
        Recupera los registros comprendidos en el rango dado
        (basado en *OFFSET* y *LIMIT*).

        Args:
            _range (tuple[int, int] | None):
                Tupla ``(offset, limit)``.  Coincide conceptualmente con
                ``page_range`` pero se pasa como tupla.
            session (sessionmaker | None, opcional):
                Sesión de SQLAlchemy a reutilizar.

        Returns:
            dict: estructura análoga a :py:meth:`getlist_numerated`.

        Raises:
            ValueError: si ``_range`` es ``None`` o no tiene exactamente
            dos elementos.
        """

        time_exec_init = time.perf_counter()

        start, fin = _range

        sql, params = self.get_sql_select()
        sql = range_row_query(sql, offset=start, limit=fin)
        counter_query = counter_row_query(sql)

        time_count_init = time.perf_counter()
        count = self.fetch_all(counter_query, params, sess=session)
        time_count = time.perf_counter() - time_count_init

        time_result_init = time.perf_counter()
        result_set = self.fetch_all(sql, params, sess=session)
        result_models = self.model.from_list(result_set)
        time_result = time.perf_counter() - time_result_init

        time_exec = time.perf_counter() - time_exec_init

        result_dict = {
            "result": result_models,
            "result_set": result_set,
            "count": count,
            "time": {
                "time_result": time_result,
                "time_count": time_count,
                "time_exec": time_exec,
            }
        }

        return result_dict

    def insert_model(self, objmodel: object|None=None, session: sessionmaker|None=None):
        """
        Inserta una instancia del modelo en la base de datos.

        Args:
            objmodel (object): Instancia del modelo a insertar.
        """
        sql, _ = self.get_sql_insert()
        if hasattr(self, "before_insert"):
            objmodel = self.before_insert(objmodel, session=session)
        params = objmodel.to_dict()
        self.execute(sql, params, session=session)
        if hasattr(self, "after_insert"):
            objmodel = self.after_insert(objmodel, session=session)

    def update_model(self, objmodel: object|None=None, session: sessionmaker|None=None):
        """
        Actualiza una instancia del modelo en la base de datos.

        Args:
            objmodel (object): Instancia del modelo a actualizar.
        """
        sql, _ = self.get_sql_update()
        if hasattr(self, "before_update"):
            objmodel = self.before_update(objmodel, session=session)
        params = objmodel.to_dict()
        self.execute(sql, params, session=session)
        if hasattr(self, "after_update"):
            objmodel = self.after_update(objmodel, session=session)

    def delete_model(self, objmodel: object|None=None, session: sessionmaker|None=None):
        """
        Elimina una instancia del modelo en la base de datos.

        Args:
            objmodel (object): Instancia del modelo a eliminar.
        """
        sql, _ = self.get_sql_delete()
        if hasattr(self, "before_delete"):
            objmodel = self.before_delete(objmodel, session=session)
        params = objmodel.to_dict()
        self.execute(sql, params, session=session)
        if hasattr(self, "after_delete"):
            self.after_delete(objmodel, session=session)

    def before_insert(self, objmodel: object|None=None, session: sessionmaker|None=None):
        """Hook opcional: lógica previa a un INSERT."""
        return objmodel

    def after_insert(self, objmodel: object|None=None, session: sessionmaker|None=None):
        """Hook opcional: lógica posterior a un INSERT."""
        return objmodel

    def before_update(self, objmodel: object|None=None, session: sessionmaker|None=None):
        """Hook opcional: lógica previa a un UPDATE."""
        return objmodel

    def after_update(self, objmodel: object|None=None, session: sessionmaker|None=None):
        """Hook opcional: lógica posterior a un UPDATE."""
        return objmodel

    def before_delete(self, objmodel: object|None=None, session: sessionmaker|None=None):
        """Hook opcional: lógica previa a un DELETE."""
        return objmodel

    def after_delete(self, objmodel: object|None=None, session: sessionmaker|None=None):
        """Hook opcional: lógica posterior a un DELETE."""
        return objmodel
    
    def call_procedure(self, proc_name:str, params: dict|None=None, session: sessionmaker|None=None):
        """
        Ejecuta un procedimiento almacenado en Oracle.

        Args:
            proc_name (str): Nombre del procedimiento.
            params (dict, opcional): Parámetros a pasar. Admite entrada y salida.

        Ejemplo:
            call_procedure("my_proc", {"p_id": 1, "p_out": outparam})
        """
        params = params or {}
        if not isinstance(params, dict):
            raise ValueError("Los parámetros deben ser un diccionario")

        placeholders = ', '.join(f':{k}' for k in params)
        sql = f"BEGIN {proc_name}({placeholders}); END;"

        if session:
            session.execute(sql, params)
        else:
            with self.session_scope() as session:
                session.execute(sql, params)

    def call_function(self, func_name:str, params: dict|None=None, session: sessionmaker|None=None):
        """
        Ejecuta una función almacenada que retorna un escalar.

        Args:
            func_name (str): Nombre de la función.
            params (dict, opcional): Parámetros de entrada.
    
        Returns:
            Resultado de la función (valor escalar).
        """
        params = params or {}
        if not isinstance(params, dict):
            raise ValueError("Los parámetros deben ser un diccionario")

        placeholders = ', '.join(f':{k}' for k in params)
        sql = f"SELECT {func_name}({placeholders}) AS result FROM DUAL"

        result = self.fetch_one(sql, params, sess=session)
        return result.get('result') if result else None
