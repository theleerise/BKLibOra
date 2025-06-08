from copy import copy
from BKLibOra.BKOraModel.BKOraDataType import BKString, BKNumber, BKFloat, BKDate, BKDatetime, BKBytes

class BKOraModelComplex:
    """
    Modelo que usa columnas ‘ricas’ BKString, BKNumber, BKFloat…
    Declaras el modelo igual que antes pero con esas clases.
    """

    # Registra aquí todos los tipos de columna aceptados
    _FIELD_TYPES = (
        BKString
        , BKNumber
        , BKFloat
        , BKDate
        , BKDatetime
        , BKBytes
    )

    # ----------  creación ----------
    def __init__(self, **kwargs):
        """
        kwargs trae los pares {nombre_columna: valor} obtenidos de la BD.
        Para cada atributo-plantilla de la clase:
          – se clona con el valor recibido,
          – se guarda en la instancia (self.<attr>).
        """
        for attr_name, field_template in self.__class__.__dict__.items():
            if isinstance(field_template, self._FIELD_TYPES):
                col_name = field_template.name or attr_name
                raw_value = kwargs.get(col_name, None)
                # Clonamos la plantilla con el valor
                field_instance = field_template.clone_with_value(raw_value)
                # Sustituimos en la instancia
                setattr(self, attr_name, field_instance)

    # ----------  serialización ----------
    def to_dict(self):
        """Devuelve {nombre_columna: valor}."""
        result = {}
        for attr_name, field_template in self.__class__.__dict__.items():
            if isinstance(field_template, self._FIELD_TYPES):
                col_name = field_template.name or attr_name
                field_instance = getattr(self, attr_name, None)
                result[col_name] = (
                    field_instance.value if field_instance else None
                )
        return result

    @classmethod
    def from_dict(cls, data_dict):
        return cls(**data_dict)

    @classmethod
    def from_list(cls, data_list):
        """Convierte una lista de dicts (rows) en objs."""
        return [cls.from_dict(row) for row in data_list]

    # ----------  introspección ----------
    @classmethod
    def get_columns_info(cls):
        """
        Devuelve {nombre_columna: {…metadata…}}
        útil para generar ‘CREATE TABLE’, validaciones externas, etc.
        """
        info = {}
        for attr_name, field_template in cls.__dict__.items():
            if isinstance(field_template, cls._FIELD_TYPES):
                col_name = field_template.name or attr_name
                # vars() da los atributos públicos del objeto
                meta = {k: v for k, v in vars(field_template).items()
                        if not k.startswith('_') and k != 'value'}
                meta['attribute'] = attr_name
                info[col_name] = meta
        return info

    # ----------  representación ----------
    def __repr__(self):
        pk_parts = []
        for attr_name, field_template in self.__class__.__dict__.items():
            if isinstance(field_template, self._FIELD_TYPES) and field_template.primary_key:
                field_instance = getattr(self, attr_name, None)
                value = field_instance.value if field_instance else None
                pk_parts.append(f"{attr_name}={value}")
        if pk_parts:
            return f"{self.__class__.__name__}: " + ", ".join(pk_parts)
        return self.__class__.__name__
