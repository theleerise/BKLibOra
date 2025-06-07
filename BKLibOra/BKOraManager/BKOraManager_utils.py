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
