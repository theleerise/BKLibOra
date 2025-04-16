from BKLibOra.BKOraModel.BKOraModelDB import BKOraModelDB
from BKLibOra.BKOraModel.BKOraModel_utils.BKOraColums import BKOraColumn

class ModelAllTableDependencies(BKOraModelDB):
    table_name = BKOraColumn(name="table_name", type_=str, primary_key=True)
    column_name = BKOraColumn(name="column_name", type_=str, primary_key=True)
    constraint_name = BKOraColumn(name="constraint_name", type_=str, primary_key=True)
    referenced_table = BKOraColumn(name="referenced_table", type_=str)
    referenced_column = BKOraColumn(name="referenced_column", type_=str)