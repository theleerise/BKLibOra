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
from abc import ABC, abstractmethod


class BKOraManagerDB(BKOraManager):
    """
    Clase base abstracta para manejar operaciones CRUD sobre una tabla Oracle usando un modelo.

    Esta clase delega la ejecución SQL a `BKOraManager` y delega la definición de sentencias SQL
    al desarrollador que herede esta clase, a través de métodos abstractos.

    Args:
        connector (BKOraConnect): Conector a la base de datos.
        model (object): Clase modelo con métodos `to_dict()` y `from_list()`.

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

    def __init__(self, connector, model):
        """
        Inicializa una instancia de BKOraManagerDB.

        Args:
            connector (BKOraConnect): Conector con método `get_session()`.
            model (object): Clase modelo con `to_dict()` y `from_list()`.
        """
        super().__init__(connector=connector)
        self.model = model

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

    def getlist(self):
        """
        Ejecuta la consulta SELECT definida por `get_sql_select()` y convierte los resultados a modelos.

        Returns:
            list[object]: Lista de instancias del modelo definido.
        """
        sql, params = self.get_sql_select()
        results = self.fetch_all(sql, params)
        return self.model.from_list(results)

    def insert_model(self, objmodel=None):
        """
        Inserta una instancia del modelo en la base de datos.

        Args:
            objmodel (object): Instancia del modelo a insertar.
        """
        sql, _ = self.get_sql_insert()
        params = objmodel.to_dict()
        if hasattr(self, "before_insert"):
            self.before_insert(params)
        self.execute(sql, params)
        if hasattr(self, "after_insert"):
            self.after_insert(params)

    def update_model(self, objmodel=None):
        """
        Actualiza una instancia del modelo en la base de datos.

        Args:
            objmodel (object): Instancia del modelo a actualizar.
        """
        sql, _ = self.get_sql_update()
        params = objmodel.to_dict()
        if hasattr(self, "before_update"):
            self.before_update(params)
        self.execute(sql, params)
        if hasattr(self, "after_update"):
            self.after_update(params)

    def delete_model(self, objmodel=None):
        """
        Elimina una instancia del modelo en la base de datos.

        Args:
            objmodel (object): Instancia del modelo a eliminar.
        """
        sql, _ = self.get_sql_delete()
        params = objmodel.to_dict()
        if hasattr(self, "before_delete"):
            self.before_delete(params)
        self.execute(sql, params)
        if hasattr(self, "after_delete"):
            self.after_delete(params)

    def before_insert(self, params):
        """Hook opcional: lógica previa a un INSERT."""
        pass

    def after_insert(self, params):
        """Hook opcional: lógica posterior a un INSERT."""
        pass

    def before_update(self, params):
        """Hook opcional: lógica previa a un UPDATE."""
        pass

    def after_update(self, params):
        """Hook opcional: lógica posterior a un UPDATE."""
        pass

    def before_delete(self, params):
        """Hook opcional: lógica previa a un DELETE."""
        pass

    def after_delete(self, params):
        """Hook opcional: lógica posterior a un DELETE."""
        pass
    
    def call_procedure(self, proc_name, params=None):
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

        with self.session_scope() as session:
            session.execute(sql, params)

    def call_function(self, func_name, params=None):
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

        result = self.fetch_one(sql, params)
        return result.get('result') if result else None
