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
