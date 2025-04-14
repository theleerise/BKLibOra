from BKLibOra.BKOraModel.BKOraModel_utils.BKOraColums import BKOraColumn

class BKOraModelDB:
    def __init__(self, **kwargs):
        for key, column in self.__class__.__dict__.items():
            if isinstance(column, BKOraColumn):
                value = kwargs.get(column.name or key, column.default)
                setattr(self, key, value)

    def to_dict(self):
        result = {}
        for key, column in self.__class__.__dict__.items():
            if isinstance(column, BKOraColumn):
                result[column.name or key] = getattr(self, key, column.default)
        return result

    @classmethod
    def from_dict(cls, data_dict):
        return cls(**data_dict)

    @classmethod
    def from_list(cls, data_list):
        return [cls.from_dict(item) for item in data_list]
