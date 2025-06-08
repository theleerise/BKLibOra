from BKLibOra.BKOraModel.BKOraModelDB import BKOraModelDB
from BKLibOra.BKOraModel.BKOraColums import BKOraColumn

class ModelJobScheduler_DetailsWithProgramAndSchedule(BKOraModelDB):
    job_name = BKOraColumn(name="job_name", type_=str, primary_key=True)
    owner = BKOraColumn(name="owner", type_=str, primary_key=True)
    state = BKOraColumn(name="state", type_=str)
    enabled = BKOraColumn(name="enabled", type_=str)
    start_date = BKOraColumn(name="start_date", type_="datetime")
    next_run_date = BKOraColumn(name="next_run_date", type_="datetime")
    repeat_interval = BKOraColumn(name="repeat_interval", type_=str)
    schedule_name = BKOraColumn(name="schedule_name", type_=str)
    program_name = BKOraColumn(name="program_name", type_=str)
    
    program_type = BKOraColumn(name="program_type", type_=str)
    program_action = BKOraColumn(name="program_action", type_=str)
    
    last_run_status = BKOraColumn(name="last_run_status", type_=str)
    actual_start_date = BKOraColumn(name="actual_start_date", type_="datetime")
    run_duration = BKOraColumn(name="run_duration", type_=str)
    
    schedule_type = BKOraColumn(name="schedule_type", type_=str)
    schedule_start = BKOraColumn(name="schedule_start", type_="datetime")
    schedule_repeat = BKOraColumn(name="schedule_repeat", type_=str)
