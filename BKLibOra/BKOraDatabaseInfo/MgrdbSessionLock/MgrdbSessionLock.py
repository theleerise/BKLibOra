from BKLibOra.BKOraManager.BKOraManagerDB import BKOraManagerDB
from BKLibOra.BKOraDatabaseInfo.MgrdbSessionLock.ModelSessionLock import ModelSessionLock

class MgrdbSessionLock(BKOraManagerDB):
    def __init__(self, connector):
        super().__init__(connector=connector, model=ModelSessionLock)

    def get_sql_select(self):
        sql = """
            SELECT
                  L1.SID AS HOLDING_SESSION
                , L2.SID AS WAITING_SESSION
                , L1.ID1
                , L1.ID2
                , L1.TYPE
                , L1.LMODE
                , L2.REQUEST
            FROM V$LOCK L1
            JOIN V$LOCK L2 ON L1.ID1 = L2.ID1 AND L1.ID2 = L2.ID2
            WHERE L1.BLOCK = 1 AND L2.REQUEST > 0
        """
        return sql, {}