from BKLibOra.config import PAGE_VALUES
from BKLibOra.BKOraManager.BKOraManager import BKOraManager
from BKLibOra.BKOraManager.BKOraManager_utils import wrapper_where_query, counter_row_query, range_row_query, BKOraRoutineExecutor
from BKLibOra.BKOraManager.BKOraQueryBuilder import BKOraQueryBuilder
from sqlalchemy.orm import sessionmaker
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple
import time
import copy

class BKOraManagerDB(BKOraManager, BKOraRoutineExecutor):
    
    DEFAULT_KWARGS = copy.deepcopy(PAGE_VALUES)
    
    def __init__(self, connector, model, *args, **kwargs):
        
        super().__init__(connector=connector)
        self.model = model
        self.args = args
        self.kwargs = self.DEFAULT_KWARGS | kwargs
        self.QueryBuilder = BKOraQueryBuilder
        
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

    def getlist(self, filter: List[Dict[str, Any]]
                , params: List[Dict[str, Any]]
                , session: sessionmaker|None=None
                , _close_sess: bool=False) -> dict:
        """
        Ejecuta la consulta SELECT definida por `get_sql_select()` y convierte los resultados a modelos.

        Returns:
            list[object]: Lista de instancias del modelo definido.
        """
        sql, _ = self.get_sql_select()
        sql = wrapper_where_query(sql)

        qb = self.QueryBuilder(base_sql=sql, filters=filter, values=params)
        sql, params = qb.build()
        
        results = self.fetch_all(sql, params, sess=session)

        if session and _close_sess:
            session.close()

        return self.model.from_list(results)
    
    def getlist_numerated(self, filter: List[Dict[str, Any]]
                          , params: List[Dict[str, Any]]
                          , session: sessionmaker|None=None
                          , _close_sess: bool=False) -> dict:
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

        sql, _ = self.get_sql_select()
        sql = wrapper_where_query(sql)

        qb = self.QueryBuilder(base_sql=sql, filters=filter, values=params)
        sql, params = qb.build()

        counter_query = counter_row_query(sql)

        time_count_init = time.perf_counter()
        count = self.fetch_one(counter_query, params, sess=session)
        time_count = time.perf_counter() - time_count_init

        time_result_init = time.perf_counter()
        result_set = self.fetch_all(sql, params, sess=session)
        result_models = self.model.from_list(result_set)
        time_result = time.perf_counter() - time_result_init

        time_exec = time.perf_counter() - time_exec_init

        result_dict = {
            "result": result_models,
            "result_set": result_set,
            "count": count.get("counter"),
            "time": {
                "time_result": time_result,
                "time_count": time_count,
                "time_exec": time_exec,
            }
        }

        if session and _close_sess:
            session.close()

        return result_dict

    def getlist_paginated(self, filter: List[Dict[str, Any]]
                          , params: List[Dict[str, Any]]
                          , session: sessionmaker|None=None
                          , _close_sess: bool=False) -> dict:
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

        sql, _ = self.get_sql_select()
        sql = wrapper_where_query(sql)

        qb = self.QueryBuilder(base_sql=sql, filters=filter, values=params)
        sql, params = qb.build()
        counter_query = counter_row_query(sql)

        time_count_init = time.perf_counter()
        count = self.fetch_one(counter_query, params, sess=session)
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
            "count": count.get("counter"),
            "time": {
                "time_page": time_page,
                "time_result": time_result,
                "time_count": time_count,
                "time_exec": time_exec,
            }
        }

        if session and _close_sess:
            session.close()

        return result_dict

    def getlist_page(self, filter: List[Dict[str, Any]]
                     , params: List[Dict[str, Any]]
                     , page_range: dict|None=None
                     , session: sessionmaker|None=None
                     , _close_sess: bool=False) -> dict:
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

        sql, _ = self.get_sql_select()
        sql = wrapper_where_query(sql)

        qb = self.QueryBuilder(base_sql=sql, filters=filter, values=params)
        sql, params = qb.build()
        counter_query = counter_row_query(sql)

        time_count_init = time.perf_counter()
        count = self.fetch_one(counter_query, params, sess=session)
        time_count = time.perf_counter() - time_count_init

        time_result_init = time.perf_counter()
        sql = range_row_query(sql, offset=page_range.get("page_init"), limit=page_range.get("page_fin"))
        result_set = self.fetch_all(sql, params, sess=session)
        result_models = self.model.from_list(result_set)
        time_result = time.perf_counter() - time_result_init

        time_exec = time.perf_counter() - time_exec_init

        result_dict = {
            "result": result_models,
            "result_set": result_set,
            "count": count.get("counter"),
            "time": {
                "time_result": time_result,
                "time_count": time_count,
                "time_exec": time_exec,
            }
        }

        if session and _close_sess:
            session.close()

        return result_dict

    def getlist_range(self, filter: List[Dict[str, Any]]
                      , params: List[Dict[str, Any]]
                      , _range: tuple|None=None
                      , session: sessionmaker|None=None
                      , _close_sess: bool=False) -> dict:
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

        sql, _ = self.get_sql_select()
        sql = wrapper_where_query(sql)

        qb = self.QueryBuilder(base_sql=sql, filters=filter, values=params)
        sql, params = qb.build()
        counter_query = counter_row_query(sql)

        time_count_init = time.perf_counter()
        count = self.fetch_one(counter_query, params, sess=session)
        time_count = time.perf_counter() - time_count_init

        time_result_init = time.perf_counter()
        sql = range_row_query(sql, offset=start, limit=fin)
        result_set = self.fetch_all(sql, params, sess=session)
        result_models = self.model.from_list(result_set)
        time_result = time.perf_counter() - time_result_init

        time_exec = time.perf_counter() - time_exec_init

        result_dict = {
            "result": result_models,
            "result_set": result_set,
            "count": count.get("counter"),
            "time": {
                "time_result": time_result,
                "time_count": time_count,
                "time_exec": time_exec,
            }
        }

        if session and _close_sess:
            session.close()

        return result_dict

    def insert_model(self, objmodel: object|None=None
                     , dict_value: dict|None=None
                     , session: sessionmaker|None=None
                     , _close_sess: bool=False
                     , only: bool=False):
        """
        Inserta una instancia del modelo en la base de datos.

        Args:
            objmodel (object): Instancia del modelo a insertar.
        """
        sql, _ = self.get_sql_insert()
        if hasattr(self, "before_insert"):
            objmodel, dict_value = self.before_insert(objmodel, dict_value, session=session)
        params = objmodel.to_dict()
        self.execute(sql, params, session=session)
        if hasattr(self, "after_insert"):
            objmodel, dict_value = self.after_insert(objmodel, dict_value, session=session)

        if session and _close_sess:
            try:
                session.commit()
            except:
                session.rollback()
            finally:
                session.close()

        if only:
            return objmodel

    def update_model(self, objmodel: object|None=None
                     , dict_value: dict|None=None
                     , session: sessionmaker|None=None
                     , _close_sess: bool=False
                     , only: bool=False):
        """
        Actualiza una instancia del modelo en la base de datos.

        Args:
            objmodel (object): Instancia del modelo a actualizar.
        """
        sql, _ = self.get_sql_update()
        if hasattr(self, "before_update"):
            objmodel, dict_value = self.before_update(objmodel, dict_value, session=session)
        params = objmodel.to_dict()
        self.execute(sql, params, session=session)
        if hasattr(self, "after_update"):
            objmodel, dict_value = self.after_update(objmodel, dict_value, session=session)

        if session and _close_sess:
            try:
                session.commit()
            except:
                session.rollback()
            finally:
                session.close()

        if only:
            return objmodel

    def delete_model(self, objmodel: object|None=None
                     , dict_value: dict|None=None
                     , session: sessionmaker|None=None
                     , _close_sess: bool=False
                     , only: bool=False):
        """
        Elimina una instancia del modelo en la base de datos.

        Args:
            objmodel (object): Instancia del modelo a eliminar.
        """
        sql, _ = self.get_sql_delete()
        if hasattr(self, "before_delete"):
            objmodel, dict_value = self.before_delete(objmodel, dict_value, session=session)
        params = objmodel.to_dict()
        self.execute(sql, params, session=session)
        if hasattr(self, "after_delete"):
            objmodel, dict_value = self.after_delete(objmodel, dict_value, session=session)

        if session and _close_sess:
            try:
                session.commit()
            except:
                session.rollback()
            finally:
                session.close()

        if only:
            return objmodel

    def before_insert(self, objmodel: object|None=None
                      , dict_value: dict|None=None
                      , session: sessionmaker|None=None):
        """Hook opcional: lógica previa a un INSERT."""
        return objmodel, dict_value

    def after_insert(self, objmodel: object|None=None
                     , dict_value: dict|None=None
                     , session: sessionmaker|None=None):
        """Hook opcional: lógica posterior a un INSERT."""
        return objmodel, dict_value

    def before_update(self, objmodel: object|None=None
                      , dict_value: dict|None=None
                      , session: sessionmaker|None=None):
        """Hook opcional: lógica previa a un UPDATE."""
        return objmodel, dict_value

    def after_update(self, objmodel: object|None=None
                     , dict_value: dict|None=None
                     , session: sessionmaker|None=None):
        """Hook opcional: lógica posterior a un UPDATE."""
        return objmodel, dict_value

    def before_delete(self, objmodel: object|None=None
                      , dict_value: dict|None=None
                      , session: sessionmaker|None=None):
        """Hook opcional: lógica previa a un DELETE."""
        return objmodel, dict_value

    def after_delete(self, objmodel: object|None=None
                     , dict_value: dict|None=None
                     , session: sessionmaker|None=None):
        """Hook opcional: lógica posterior a un DELETE."""
        return objmodel, dict_value
