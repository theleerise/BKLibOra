from BKLibOra.config import PAGE_VALUES
from BKLibOra.BKOraManager.BKOraManager import BKOraManager
from BKLibOra.BKOraManager.BKOraManager_utils import wrapper_where_query, counter_row_query, range_row_query, BKOraRoutineExecutor
from BKLibOra.BKOraManager.BKOraQueryBuilder import BKOraQueryBuilder
from sqlalchemy.orm import sessionmaker
from abc import ABC, abstractmethod
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

    def getlist(self, filter, params, session: sessionmaker|None=None) -> dict:
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
        return self.model.from_list(results)