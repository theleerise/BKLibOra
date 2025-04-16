from BKLibOra.BKOraModel.BKOraModelDB import BKOraModelDB
from BKLibOra.BKOraModel.BKOraModel_utils.BKOraColums import BKOraColumn

class ModelAllSequences(BKOraModelDB):
    sequence_owner = BKOraColumn(name="sequence_owner", type_=str, primary_key=True)
    sequence_name = BKOraColumn(name="sequence_name", type_=str, primary_key=True)
    min_value = BKOraColumn(name="min_value", type_=int)
    max_value = BKOraColumn(name="max_value", type_=int)
    increment_by = BKOraColumn(name="increment_by", type_=int)
    cycle_flag = BKOraColumn(name="cycle_flag", type_=str)
    order_flag = BKOraColumn(name="order_flag", type_=str)
    cache_size = BKOraColumn(name="cache_size", type_=int)
    cache_size = BKOraColumn(name="cache_size", type_=int)
    last_number = BKOraColumn(name="last_number", type_=int)