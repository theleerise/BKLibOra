from BKLibOra.BKOraManager.BKOraManagerDB import BKOraManagerDB
from BKLibOra.BKOraDatabaseInfo.MgrdbCurrentExecuteQuery.ModelCurrentExecuteQuery import ModelCurrentExecuteQuery

class MgrdbCurrentExecuteQuery(BKOraManagerDB):
    def __init__(self, connector):
        super().__init__(connector=connector, model=ModelCurrentExecuteQuery)

    def get_sql_select(self):
        sql = """
            SELECT 
                S.SID,
                S.SERIAL#,
                S.USERNAME,
                S.OSUSER,
                S.MACHINE,
                S.PROGRAM,
                S.STATUS,
                S.SQL_ID,
                Q.SQL_TEXT
            FROM V$SESSION S
            JOIN V$SQL Q ON S.SQL_ID = Q.SQL_ID
            WHERE S.STATUS = 'ACTIVE'
        """
        return sql, {}