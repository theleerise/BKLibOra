from BKLibOra.BKOraModel.BKOraModelDB import BKOraModelDB
from BKLibOra.BKOraModel.BKOraModel_utils.BKOraColums import BKOraColumn

class ModelTableStructure(BKOraModelDB):
    owner = BKOraColumn(name="owner", type_=str, primary_key=True)
    table_name = BKOraColumn(name="table_name", type_=str, primary_key=True)
    column_name = BKOraColumn(name="column_name", type_=str, primary_key=True)
    data_type = BKOraColumn(name="data_type", type_=str)
    data_length = BKOraColumn(name="data_length", type_=int)
    data_precision = BKOraColumn(name="data_precision", type_=int)
    data_scale = BKOraColumn(name="data_scale", type_=int)
    nullable = BKOraColumn(name="nullable", type_=str)
    primary_key = BKOraColumn(name="primary_key", type_=str)
    comments = BKOraColumn(name="comments", type_=str)
