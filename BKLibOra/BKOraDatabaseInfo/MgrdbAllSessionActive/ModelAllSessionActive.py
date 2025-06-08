from BKLibOra.BKOraModel.BKOraModelDB import BKOraModelDB
from BKLibOra.BKOraModel.BKOraColums import BKOraColumn

class ModelAllSessionActive(BKOraModelDB):
    sid = BKOraColumn(name="sid", type_=int, primary_key=True)
    serial_number = BKOraColumn(name="serial#", type_=int, primary_key=True)
    username = BKOraColumn(name="username", type_=str)
    status = BKOraColumn(name="status", type_=str)
    program = BKOraColumn(name="program", type_=str)
    module = BKOraColumn(name="module", type_=str)
    machine = BKOraColumn(name="machine", type_=str)
    logon_time = BKOraColumn(name="logon_time", type_="datetime")
    sql_id = BKOraColumn(name="sql_id", type_=str)
    sql_text = BKOraColumn(name="sql_text", type_=str)
