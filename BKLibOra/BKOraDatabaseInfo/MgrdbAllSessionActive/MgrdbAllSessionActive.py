from BKLibOra.BKOraManager.BKOraManagerDB import BKOraManagerDB
from BKLibOra.BKOraDatabaseInfo.MgrdbAllSessionActive.ModelAllSessionActive import ModelAllSessionActive

class MgrdbAllSessionActive(BKOraManagerDB):
    def __init__(self, connector):
        super().__init__(connector=connector, model=ModelAllSessionActive)

    def get_sql_select(self):
        sql = """
            SELECT
                S.SID,
                S.SERIAL#,
                S.USERNAME,
                S.STATUS,
                S.PROGRAM,
                S.MODULE,
                S.MACHINE,
                S.LOGON_TIME,
                S.SQL_ID,
                Q.SQL_TEXT
            FROM V$SESSION S
            LEFT JOIN V$SQL Q ON S.SQL_ID = Q.SQL_ID
        """
        return sql, {}