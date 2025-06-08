from BKLibOra.BKOraModel.BKOraModelDB import BKOraModelDB
from BKLibOra.BKOraModel.BKOraColums import BKOraColumn

class ModelCurrentExecuteQuery(BKOraModelDB):
    sid = BKOraColumn(name="sid", type_=int, primary_key=True)
    serial_number = BKOraColumn(name="serial#", type_=int, primary_key=True)
    username = BKOraColumn(name="username", type_=str)
    osuser = BKOraColumn(name="osuser", type_=str)
    machine = BKOraColumn(name="machine", type_=str)
    program = BKOraColumn(name="program", type_=str)
    status = BKOraColumn(name="status", type_=str)
    sql_id = BKOraColumn(name="sql_id", type_=str)
    sql_text = BKOraColumn(name="sql_text", type_=str)
