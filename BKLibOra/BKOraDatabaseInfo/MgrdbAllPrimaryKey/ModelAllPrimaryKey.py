from BKLibOra.BKOraModel.BKOraModelDB import BKOraModelDB
from BKLibOra.BKOraModel.BKOraColums import BKOraColumn

class ModelAllPrimaryKey(BKOraModelDB):
    table_name = BKOraColumn(name="table_name", type_=str, primary_key=True)
    column_name = BKOraColumn(name="column_name", type_=str)
    posicion = BKOraColumn(name="posicion", type_=int)
    constraint_name = BKOraColumn(name="constraint_name", type_=str, primary_key=True)
