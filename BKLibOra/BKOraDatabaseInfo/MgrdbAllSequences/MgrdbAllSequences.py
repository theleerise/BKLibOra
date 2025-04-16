from BKLibOra.BKOraManager.BKOraManagerDB import BKOraManagerDB
from BKLibOra.BKOraDatabaseInfo.MgrdbAllSequences.ModelAllSequences import ModelAllSequences

class MgrdbAllSequences(BKOraManagerDB):
    def __init__(self, connector):
        super().__init__(connector=connector, model=ModelAllSequences)

    def get_sql_select(self):
        sql = """
            SELECT 
                  SEQUENCE_OWNER
                , SEQUENCE_NAME
                , MIN_VALUE
                , MAX_VALUE
                , INCREMENT_BY
                , CYCLE_FLAG
                , ORDER_FLAG
                , CACHE_SIZE
                , LAST_NUMBER
            FROM ALL_SEQUENCES
        """
        return sql, {}