from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from BKLibOra.BKOraManager.BKOraManager import BKOraManager
from BKLibOra.BKOraManager.BKOraQueryBuilder import BKOraQueryBuilder


class BKOraDynamicManager(BKOraManager):
    """Gestor avanzado de consultas dinámicas para Oracle.

    Extiende :class:`BKOraManager` combinándolo con :class:`BKOraQueryBuilder` para
    permitir la construcción de *WHERE* dinámicos basados en reglas y valores
    suministrados en tiempo de ejecución.

    Funciona en tres pasos internos:

    1. **Construcción del SQL final** mediante ``BKOraQueryBuilder`` si se
       proporcionan *filters* / *values*.
    2. **Combinación de parámetros** (los del *QueryBuilder* + *params* extra).
    3. **Ejecución** mediante los métodos de la superclase (``fetch_all``,
       ``fetch_one`` o ``execute``).

    Args:
        connector: Instancia de :class:`BKOraConnect` con método
            ``get_session()``.
    """

    # ------------------------------------------------------------------ #
    # API pública – helpers de alto nivel
    # ------------------------------------------------------------------ #
    def fetch_all(
        self,
        base_sql: str,
        params: Optional[Dict[str, Any]] = None,
        *,
        filters: Optional[List[Dict[str, Any]]] = None,
        values: Optional[List[Dict[str, Any]]] = None,
        sess=None,
    ) -> List[Dict[str, Any]]:
        """Ejecuta un SELECT devolviendo todas las filas con filtros dinámicos.

        Args:
            base_sql: Sentencia SQL base (sin WHERE o con WHERE inicial).
            params: Parámetros adicionales para enlazar (sobrescriben si
                colisionan con los generados por ``BKOraQueryBuilder``).
            filters: Lista de reglas de filtrado (ver ``BKOraQueryBuilder``).
            values: Valores asociados a los filtros.
            sess: Sesión SQLAlchemy abierta opcional (para transacciones).

        Returns:
            Lista de filas (dict por columna).
        """
        sql, final_params = self._build_query(base_sql, filters, values, params)
        return super().fetch_all(sql, final_params, sess=sess)

    def fetch_one(
        self,
        base_sql: str,
        params: Optional[Dict[str, Any]] = None,
        *,
        filters: Optional[List[Dict[str, Any]]] = None,
        values: Optional[List[Dict[str, Any]]] = None,
        sess=None,
    ) -> Optional[Dict[str, Any]]:
        """Ejecuta un SELECT devolviendo la primera fila que cumpla los filtros.
        """
        sql, final_params = self._build_query(base_sql, filters, values, params)
        return super().fetch_one(sql, final_params, sess=sess)

    def execute(
        self,
        base_sql: str,
        params: Optional[Dict[str, Any]] = None,
        *,
        filters: Optional[List[Dict[str, Any]]] = None,
        values: Optional[List[Dict[str, Any]]] = None,
        sess=None,
    ) -> None:
        """Ejecuta un DML (INSERT/UPDATE/DELETE) con filtros dinámicos.
        """
        sql, final_params = self._build_query(base_sql, filters, values, params)
        super().execute(sql, final_params, sess=sess)

    # ------------------------------------------------------------------ #
    # Lógica interna
    # ------------------------------------------------------------------ #
    def _build_query(
        self,
        base_sql: str,
        filters: Optional[List[Dict[str, Any]]],
        values: Optional[List[Dict[str, Any]]],
        extra_params: Optional[Dict[str, Any]],
    ) -> Tuple[str, Dict[str, Any]]:
        """Construye el SQL final y el diccionario de parámetros.

        1. Si se aportan *filters* y *values*, se usa ``BKOraQueryBuilder``.
        2. Combina los parámetros generados con *extra_params* (si existen,
           estas últimas prevalecen en caso de duplicidad).
        """
        if filters and values:
            qb = BKOraQueryBuilder(base_sql, filters=filters, values=values)
            sql, qb_params = qb.build()
        else:
            sql, qb_params = base_sql, {}

        final_params: Dict[str, Any] = {}
        final_params.update(qb_params)
        if extra_params:
            final_params.update(extra_params)

        return sql, final_params


'''
# 1)  Conexión a la base de datos -------------------------------------------------
#    (cambia usuario, contraseña y DSN por los tuyos)
connector = BKOraConnect(user="USR", password="PWD", dsn="host:1521/ORCL")

# 2)  Instanciar el manager dinámico ---------------------------------------------
dm = BKOraDynamicManager(connector)

# -------------------------------------------------------------------------------
#    EJEMPLO 1 – SELECT con filtros "IN" y "BETWEEN"
# -------------------------------------------------------------------------------
base_sql = """
    SELECT id_pedido, cliente, fecha, estado
    FROM pedidos
    WHERE 1 = 1            -- placeholder para filtros dinámicos
"""

filters = [
    {"column": "estado"},                                      # IN (varios valores)
    {"column": "fecha", "condition": {"operator": "between"}}, # BETWEEN
]
values = [
    {"estado": "ACTIVO"}, {"estado": "PENDIENTE"},             # -> IN (:estado, :estado_copy1)
    {"fecha": "2025-01-01"}, {"fecha": "2025-01-31"},          # -> BETWEEN :fecha AND :fecha_copy1
]

rows = dm.fetch_all(base_sql, filters=filters, values=values)
print("Pedidos filtrados:")
for r in rows:
    print(r)

# -------------------------------------------------------------------------------
#    EJEMPLO 2 – Obtiene un único registro con LIKE + función UPPER
# -------------------------------------------------------------------------------
sql_cliente = """
    SELECT id_cliente, nombre, email
    FROM clientes
    WHERE 1 = 1
"""

filters_cli = [
    {"column": "nombre", "condition": {"operator": "like", "function": "UPPER"}},
]
values_cli = [{"nombre": "%GÓMEZ%"}]

cliente = dm.fetch_one(sql_cliente, filters=filters_cli, values=values_cli)
print("\nCliente encontrado:", cliente)

# -------------------------------------------------------------------------------
#    EJEMPLO 3 – UPDATE dinámico dentro de una misma transacción
# -------------------------------------------------------------------------------
update_sql = """
    UPDATE pedidos
    SET estado = :nuevo_estado
    WHERE 1 = 1
"""

filters_upd = [{"column": "id_pedido"}]
values_upd  = [{"id_pedido": 12345}]

# Par extra aparte de los filtros
params_upd = {"nuevo_estado": "ENTREGADO"}

with connector.get_session() as sess:          # Transacción explícita
    dm.execute(
        update_sql,
        params=params_upd,
        filters=filters_upd,
        values=values_upd,
        sess=sess,                             # Reutilizamos la misma sesión
    )
    # Si quieres revisar el cambio antes del commit, haz otro SELECT aquí
    # … y decides si haces sess.commit() o sess.rollback()

'''