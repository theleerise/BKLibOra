from __future__ import annotations

from collections import defaultdict
from typing import Any, Dict, List, Tuple


class BKOraQueryBuilder:
    """
    Builder para componer consultas SQL con filtros dinámicos,
    incluyendo operadores BETWEEN, IN, =, >, etc.

    Ejemplo de uso:
        qb = BKOraQueryBuilder(
            base_sql,
            filters=[{"column": "fecha", "condition": {"operator": "between"}}],
            values=[{"fecha": "2025-01-01"}, {"fecha": "2025-01-31"}],
        )
        final_sql, params = qb.build()
    """

    _OPERATOR_MAP = {
        "equal": "=",
        "not_equal": "!=",
        "gt": ">",
        "gte": ">=",
        "lt": "<",
        "lte": "<=",
        "like": "LIKE",
        "in": "IN",          # se fuerza si llegan >1 valores con "equal"
        "between": "BETWEEN",
    }

    def __init__(
        self,
        base_sql: str,
        filters: List[Dict[str, Any]],
        values: List[Dict[str, Any]],
    ) -> None:
        self.base_sql = base_sql.rstrip()
        self.filters = filters
        self.values = values

        self._bind_counter: Dict[str, int] = defaultdict(int)
        self._params: Dict[str, Any] = {}
        self._where_clauses: List[str] = []

    # ------------------------------------------------------------------ #
    # API pública
    # ------------------------------------------------------------------ #
    def build(self) -> Tuple[str, Dict[str, Any]]:
        """Devuelve (sql_transformada, params_dict)."""
        for rule in self.filters:
            column = rule["column"]
            cond = rule.get("condition", {})
            operator = cond.get("operator", "equal").lower()
            func = cond.get("function", "").strip().upper()

            vals = self._extract_column_values(column)
            if not vals:
                continue

            sql_column = f"{func}({column})" if func else column

            if operator == "between":
                self._handle_between(sql_column, column, vals)
            elif len(vals) == 1 and operator != "in":
                self._handle_single(sql_column, column, vals[0], operator)
            else:
                self._handle_in(sql_column, column, vals)

        sql = "\n".join([self.base_sql, *self._where_clauses])
        return sql, self._params

    # ------------------------------------------------------------------ #
    # Implementación interna
    # ------------------------------------------------------------------ #
    def _extract_column_values(self, column: str) -> List[Any]:
        return [entry[column] for entry in self.values if column in entry]

    def _next_bind(self, column: str) -> str:
        count = self._bind_counter[column]
        self._bind_counter[column] += 1
        return f"{column}" if count == 0 else f"{column}_copy{count}"

    # --- Operadores ---------------------------------------------------- #
    def _handle_single(self, sql_col: str, column: str, value: Any, op: str) -> None:
        bind = self._next_bind(column)
        self._params[bind] = value
        sql_op = self._OPERATOR_MAP.get(op, "=")
        self._where_clauses.append(f"AND {sql_col} {sql_op} :{bind}")

    def _handle_in(self, sql_col: str, column: str, values: List[Any]) -> None:
        bind_names = []
        for val in values:
            bind = self._next_bind(column)
            self._params[bind] = val
            bind_names.append(f":{bind}")
        placeholders = ", ".join(bind_names)
        self._where_clauses.append(f"AND {sql_col} IN ({placeholders})")

    def _handle_between(self, sql_col: str, column: str, values: List[Any]) -> None:
        if len(values) != 2:
            raise ValueError(
                f"El operador BETWEEN requiere exactamente 2 valores para '{column}', "
                f"pero se recibieron {len(values)}."
            )
        lower_bind = self._next_bind(column)
        upper_bind = self._next_bind(column)
        self._params[lower_bind], self._params[upper_bind] = values
        clause = f"AND {sql_col} BETWEEN :{lower_bind} AND :{upper_bind}"
        self._where_clauses.append(clause)

"""
# ------------------------------------------------------------------
# Ejemplos de uso
# ------------------------------------------------------------------
examples = []

# 1. Igualdad simple
base_sql_1 = "SELECT * FROM pedidos WHERE 1=1"
filters_1 = [{"column": "estado"}]
values_1 = [{"estado": "ACTIVO"}]
qb1 = BKOraQueryBuilder(base_sql_1, filters_1, values_1)
sql1, params1 = qb1.build()
examples.append(
    {"Ejemplo": "Igualdad simple", "SQL resultante": sql1, "Parámetros": params1}
)

# 2. Filtro IN con múltiples valores
base_sql_2 = "SELECT * FROM productos WHERE 1=1"
filters_2 = [{"column": "categoria"}]
values_2 = [{"categoria": "LIBROS"}, {"categoria": "MÚSICA"}, {"categoria": "JUEGOS"}]
qb2 = BKOraQueryBuilder(base_sql_2, filters_2, values_2)
sql2, params2 = qb2.build()
examples.append(
    {"Ejemplo": "Filtro IN", "SQL resultante": sql2, "Parámetros": params2}
)

# 3. Rango BETWEEN
base_sql_3 = "SELECT * FROM ventas WHERE 1=1"
filters_3 = [{"column": "fecha", "condition": {"operator": "between"}}]
values_3 = [{"fecha": "2025-01-01"}, {"fecha": "2025-01-31"}]
qb3 = BKOraQueryBuilder(base_sql_3, filters_3, values_3)
sql3, params3 = qb3.build()
examples.append(
    {"Ejemplo": "Rango BETWEEN", "SQL resultante": sql3, "Parámetros": params3}
)

# 4. LIKE con función UPPER
base_sql_4 = "SELECT * FROM clientes WHERE 1=1"
filters_4 = [
    {"column": "nombre", "condition": {"operator": "like", "function": "UPPER"}}
]
values_4 = [{"nombre": "%GÓMEZ%"}]
qb4 = BKOraQueryBuilder(base_sql_4, filters_4, values_4)
sql4, params4 = qb4.build()
examples.append(
    {"Ejemplo": "LIKE + UPPER", "SQL resultante": sql4, "Parámetros": params4}
)
"""