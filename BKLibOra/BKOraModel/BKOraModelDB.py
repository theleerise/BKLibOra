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

    @classmethod
    def get_columns_info(cls):
        columns_info = {}
        for key, column in cls.__dict__.items():
            # Identificamos columnas por tener ciertos atributos esperados
            if hasattr(column, 'name') and hasattr(column, 'type'):
                column_name = getattr(column, 'name', key) or key
                # Tomamos todos los atributos públicos definidos en el objeto
                info_dict = {k: v for k, v in vars(column).items() if not k.startswith('_')}
                info_dict['attribute'] = key
                columns_info[column_name] = info_dict
        return columns_info

    
    def __repr__(self):
        pk_parts = []
        for attr_name in dir(self):
            attr = getattr(self.__class__, attr_name, None)
            if hasattr(attr, "primary_key") and attr.primary_key:
                value = getattr(self, attr_name, None)
                pk_parts.append(f"{attr_name}={value}")

        if pk_parts:
            pk_str = ", ".join(pk_parts)
            return f"{self.__class__.__name__}: {pk_str}"
        else:
            return f"{self.__class__.__name__}"
