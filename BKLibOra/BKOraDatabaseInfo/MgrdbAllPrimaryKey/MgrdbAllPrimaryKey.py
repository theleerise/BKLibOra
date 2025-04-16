from BKLibOra.BKOraManager.BKOraManagerDB import BKOraManagerDB
from BKLibOra.BKOraDatabaseInfo.MgrdbAllPrimaryKey.ModelAllPrimaryKey import ModelAllPrimaryKey

class MgrdbAllTableDependencies(BKOraManagerDB):
    def __init__(self, connector):
        super().__init__(connector=connector, model=ModelAllPrimaryKey)

    def get_sql_select(self):
        sql = """
            SELECT 
                  A.TABLE_NAME
                , A.COLUMN_NAME
                , A.CONSTRAINT_NAME
                , C_PK.TABLE_NAME AS REFERENCED_TABLE
                , B.COLUMN_NAME AS REFERENCED_COLUMN
            FROM ALL_CONS_COLUMNS A
            JOIN ALL_CONSTRAINTS C 
                ON A.CONSTRAINT_NAME = C.CONSTRAINT_NAME 
               AND A.OWNER = C.OWNER
            JOIN ALL_CONSTRAINTS C_PK 
                ON C.R_CONSTRAINT_NAME = C_PK.CONSTRAINT_NAME 
               AND C.R_OWNER = C_PK.OWNER
            JOIN ALL_CONS_COLUMNS B 
                ON C_PK.CONSTRAINT_NAME = B.CONSTRAINT_NAME 
               AND B.POSITION = A.POSITION
        """
        return sql, {}