from BKLibOra.BKOraManager.BKOraManagerDB import BKOraManagerDB
from BKLibOra.BKOraDatabaseInfo.MgrdbJobScheduler_StatusWithErrorInfo.ModelJobScheduler_StatusWithErrorInfo import ModelJobScheduler_StatusWithErrorInfo

class MgrdbJobScheduler_StatusWithErrorInfo(BKOraManagerDB):
    def __init__(self, connector):
        super().__init__(connector=connector, model=ModelJobScheduler_StatusWithErrorInfo)

    def get_sql_select(self):
        sql = """
            SELECT 
                  J.JOB_NAME
                , J.OWNER
                , J.JOB_TYPE
                , J.JOB_ACTION
                , J.ENABLED
                , J.STATE
                , J.START_DATE
                , J.NEXT_RUN_DATE
                , R.STATUS AS LAST_STATUS
                , R.ERROR#
                , R.ADDITIONAL_INFO
                , R.ACTUAL_START_DATE
                , R.RUN_DURATION
            FROM
                DBA_SCHEDULER_JOBS J
            LEFT JOIN (
                SELECT
                    JOB_NAME,
                    OWNER,
                    STATUS,
                    ERROR#,
                    ADDITIONAL_INFO,
                    ACTUAL_START_DATE,
                    RUN_DURATION,
                    ROW_NUMBER() OVER (PARTITION BY JOB_NAME, OWNER ORDER BY ACTUAL_START_DATE DESC) AS RN
                FROM
                    DBA_SCHEDULER_JOB_RUN_DETAILS
            ) R ON J.JOB_NAME = R.JOB_NAME AND J.OWNER = R.OWNER AND R.RN = 1
            ORDER BY
                J.NEXT_RUN_DATE
        """
        return sql, {}