from BKLibOra.BKOraManager.BKOraManagerDB import BKOraManagerDB
from BKLibOra.BKOraDatabaseInfo.MgrdbTableStructure.ModelTableStructure import ModelTableStructure

class MgrdbTableStructure(BKOraManagerDB):
    def __init__(self, connector):
        super().__init__(connector=connector, model=ModelTableStructure)

    def get_sql_select(self):
        sql = """
            SELECT 
                  C.OWNER
                , C.TABLE_NAME
                , C.COLUMN_NAME
                , C.DATA_TYPE
                , C.DATA_LENGTH
                , C.DATA_PRECISION
                , C.DATA_SCALE
                , C.NULLABLE
                , CASE WHEN PK.COLUMN_NAME IS NOT NULL THEN 'YES' ELSE 'NO' END AS PRIMARY_KEY
                , CC.COMMENTS
            FROM ALL_TAB_COLUMNS C
            LEFT JOIN (
                SELECT ACC.COLUMN_NAME
                FROM ALL_CONSTRAINTS AC
                JOIN ALL_CONS_COLUMNS ACC ON AC.CONSTRAINT_NAME = ACC.CONSTRAINT_NAME AND AC.OWNER = ACC.OWNER
                WHERE AC.CONSTRAINT_TYPE = 'P'
            ) PK ON C.COLUMN_NAME = PK.COLUMN_NAME
            LEFT JOIN ALL_COL_COMMENTS CC ON C.OWNER = CC.OWNER AND C.TABLE_NAME = CC.TABLE_NAME AND C.COLUMN_NAME = CC.COLUMN_NAME
            ORDER BY C.OWNER, C.TABLE_NAME, C.COLUMN_ID
        """
        return sql, {}