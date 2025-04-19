from BKLibOra.BKOraManager.BKOraManagerDB import BKOraManagerDB
from BKLibOra.BKOraDatabaseInfo.MgrdbJobScheduler_DetailsWithProgramAndSchedule.ModelJobScheduler_DetailsWithProgramAndSchedule import ModelJobScheduler_DetailsWithProgramAndSchedule

class MgrdbJobScheduler_DetailsWithProgramAndSchedule(BKOraManagerDB):
    def __init__(self, connector):
        super().__init__(connector=connector, model=ModelJobScheduler_DetailsWithProgramAndSchedule)

    def get_sql_select(self):
        sql = """
            SELECT 
                  J.JOB_NAME
                , J.OWNER
                , J.STATE
                , J.ENABLED
                , J.START_DATE
                , J.NEXT_RUN_DATE
                , J.REPEAT_INTERVAL
                , J.SCHEDULE_NAME
                , J.PROGRAM_NAME
                , P.PROGRAM_TYPE
                , P.PROGRAM_ACTION
                , R.STATUS AS LAST_RUN_STATUS
                , R.ACTUAL_START_DATE
                , R.RUN_DURATION
                , S.SCHEDULE_TYPE
                , S.START_DATE AS SCHEDULE_START
                , S.REPEAT_INTERVAL AS SCHEDULE_REPEAT
            FROM
                DBA_SCHEDULER_JOBS J
            LEFT JOIN DBA_SCHEDULER_PROGRAMS P
                ON J.PROGRAM_NAME = P.PROGRAM_NAME AND J.OWNER = P.OWNER
            LEFT JOIN (
                SELECT JOB_NAME, OWNER, STATUS, ACTUAL_START_DATE, RUN_DURATION,
                       ROW_NUMBER() OVER (PARTITION BY JOB_NAME, OWNER ORDER BY ACTUAL_START_DATE DESC) AS RN
                FROM DBA_SCHEDULER_JOB_RUN_DETAILS
            ) R ON J.JOB_NAME = R.JOB_NAME AND J.OWNER = R.OWNER AND R.RN = 1
            LEFT JOIN DBA_SCHEDULER_SCHEDULES S
                ON J.SCHEDULE_NAME = S.SCHEDULE_NAME AND J.OWNER = S.OWNER
            ORDER BY J.NEXT_RUN_DATE
        """
        return sql, {}