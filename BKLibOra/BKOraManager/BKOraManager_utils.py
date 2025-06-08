from sqlalchemy.orm import sessionmaker

def wrapper_where_query(query: str) -> str:
    """
    Envuelve una consulta SQL arbitraria dentro de un sub-select y añade un
    comodín `WHERE 1 = 1`, lo que facilita concatenar luego condiciones
    adicionales sin preocuparse por la sintaxis del primer «WHERE».

    Parameters
    ----------
    query : str
        Cadena con la consulta SQL original que se desea encapsular.

    Returns
    -------
    str
        Consulta SQL formateada, lista para ampliar con cláusulas
        `AND ...` si es necesario.

    Notes
    -----
    - `WHERE 1 = 1` es una técnica habitual para simplificar la
      generación dinámica de filtros: todas las condiciones siguientes se
      introducen simplemente con `AND`.
    - La función **no** valida ni escapa la consulta recibida; se asume
      que `query` es una cadena SQL segura y bien formada.

    Examples
    --------
    >>> raw_query = "SELECT id, nombre FROM clientes"
    >>> wrapper_where_query(raw_query)
    '\\n        SELECT * FROM (\\n            SELECT id, nombre FROM clientes\\n        ) WHERE 1=1\\n    '
    >>> # Añadir filtros dinámicos
    >>> final_query = wrapper_where_query(raw_query) + " AND fecha_alta >= :fecha_ini"
    """
    format_query = f"""
        SELECT * FROM (
            {query}
        ) WHERE 1=1
    """
    return format_query

def counter_row_query(query: str) -> str:
    """
    Genera una sub-consulta que devuelve el número total de filas
    que produciría la sentencia SQL original.

    Se envuelve la consulta recibida en un `SELECT COUNT(*) FROM (...)`
    para obtener el recuento sin necesidad de ejecutar la consulta
    completa.

    Args:
        query (str): Sentencia SQL sobre la que se desea calcular
            el número de filas resultantes.

    Returns:
        str: Cadena SQL con la sub-consulta de conteo.

    Example:
        >>> sql_base = "SELECT * FROM users WHERE active = 1"
        >>> print(counter_row_query(sql_base))
        SELECT COUNT(*) FROM (
            SELECT * FROM users WHERE active = 1
        ) QUERY_COUNT
    """
    format_query = f"""
        SELECT COUNT(*) AS COUNTER FROM (
            {query}
        ) QUERY_COUNT
    """
    return format_query

def range_row_query(query: str, offset: int, limit: int) -> str:
    """
    Añade paginación basada en `OFFSET … FETCH NEXT …` a la sentencia SQL.

    Ideal para bases de datos que soportan la sintaxis de paginación
    estilo ANSI/ISO (por ejemplo, SQL Server 2012+, Oracle 12c,
    PostgreSQL v13+ con `FETCH`).

    Args:
        query (str): Consulta SQL original sin cláusulas de paginación.
        offset (int): Número de filas que se omitirán (*OFFSET*).
        limit (int): Número máximo de filas que se devolverán
            (*FETCH NEXT … ROWS ONLY*).

    Returns:
        str: Consulta SQL paginada.

    Raises:
        ValueError: Si `offset` o `limit` son negativos.

    Example:
        >>> sql_base = "SELECT id, name FROM products ORDER BY name"
        >>> print(range_row_query(sql_base, offset=20, limit=10))
        SELECT id, name FROM products ORDER BY name
        OFFSET 20 ROWS FETCH NEXT 10 ROWS ONLY
    """
    if offset < 0 or limit < 0:
        raise ValueError("offset y limit deben ser valores no negativos")

    format_query = f"""
        {query}
        OFFSET {offset} ROWS FETCH NEXT {limit} ROWS ONLY
    """
    return format_query


class BKOraRoutineExecutor:
    """Proporciona call_procedure y call_function.

    Requiere que la clase que lo use exponga:
      * self.session_scope()
      * self.fetch_one()
    """
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