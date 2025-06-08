from BKLibOra.BKOraModel.BKOraModelDB import BKOraModelDB
from BKLibOra.BKOraModel.BKOraColums import BKOraColumn

class ModelSessionLock(BKOraModelDB):
    holding_session = BKOraColumn(name="holding_session", type_=int, primary_key=True)
    waiting_session = BKOraColumn(name="waiting_session", type_=int, primary_key=True)
    id1 = BKOraColumn(name="id1", type_=int)
    id2 = BKOraColumn(name="id2", type_=int)
    type = BKOraColumn(name="type", type_=str)
    lmode = BKOraColumn(name="lmode", type_=int)
    request = BKOraColumn(name="request", type_=int)
