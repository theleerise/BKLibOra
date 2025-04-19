from BKLibOra.BKOraModel.BKOraModelDB import BKOraModelDB
from BKLibOra.BKOraModel.BKOraModel_utils.BKOraColums import BKOraColumn

class ModelJobScheduler_StatusWithErrorInfo(BKOraModelDB):
    job_name = BKOraColumn(name="job_name", type_=str, primary_key=True)
    owner = BKOraColumn(name="owner", type_=str, primary_key=True)
    job_type = BKOraColumn(name="job_type", type_=str)
    job_action = BKOraColumn(name="job_action", type_=str)
    enabled = BKOraColumn(name="enabled", type_=str)
    state = BKOraColumn(name="state", type_=str)
    start_date = BKOraColumn(name="start_date", type_="datetime")
    next_run_date = BKOraColumn(name="next_run_date", type_="datetime")
    
    last_status = BKOraColumn(name="last_status", type_=str)
    error_number = BKOraColumn(name="error#", type_=int)
    additional_info = BKOraColumn(name="additional_info", type_=str)
    actual_start_date = BKOraColumn(name="actual_start_date", type_="datetime")
    run_duration = BKOraColumn(name="run_duration", type_=str)
