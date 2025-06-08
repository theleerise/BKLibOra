from BKLibOra.utils import get_byte_size
from BKLibOra.config import MAX_VALUES
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from datetime import datetime
from datetime import date
import copy


class BKString:

    MAX_BYTES = MAX_VALUES.get("string", 4000)  # Default max bytes for string
    
    def __init__(self
                 , name: str
                 , value: str=None
                 , large: int=MAX_BYTES
                 , min_length: int=0
                 , nullable: bool=True
                 , primary_key: bool = False
                 , doc: str=None
                 , _encoding: str="utf-8"):
        self.value = value
        self.name = name
        self.large = large
        self.min_length = min_length
        self.nullable = nullable
        self.doc = doc
        self.encoding = _encoding

        self.validate_init()

    def validate_init(self):
        self.__validate_value()

    def __validate_value(self):
        if self.value is not None:
            if not isinstance(self.value, str):
                raise TypeError(f"Expected str, got {type(self.value).__name__}")
            if self.min_length is not None and len(self.value) < self.min_length:
                raise ValueError(f"String length is less than minimum of {self.min_length}")

            _bytes = get_byte_size(data=self.value, encoding=self.encoding)

            if (_bytes > self.large) or (_bytes > BKString.MAX_BYTES):
                raise ValueError(f"String length exceeds maximum of {self.large} bytes")

    def clone_with_value(self, value):
        """Devuelve una copia de sí misma con value distinto (sin mutar la plantilla)."""
        clone = copy.copy(self)
        clone.value = value
        clone.validate_init()       # valida el nuevo valor
        return clone

    def __str__(self):
        return str(self.value) if self.value is not None else "None"


class BKNumber:
    MAX_DIGITS = MAX_VALUES.get("number", 38)

    def __init__(self
                 , name: str
                 , value: int = None
                 , large: int = MAX_DIGITS
                 , min_value: int = None
                 , max_value: int = None
                 , nullable: bool = True
                 , primary_key: bool = False
                 , doc: str = None):
        self.name = name
        self.value = value
        self.large = large
        self.min_value = min_value
        self.max_value = max_value
        self.nullable = nullable
        self.primary_key = primary_key
        self.doc = doc

        self.validate_init()

    def validate_init(self):
        self.__validate_value()

    def __validate_value(self):
        if self.value is None:
            if not self.nullable:
                raise ValueError(f"Field '{self.name}' cannot be null")
            return

        if not isinstance(self.value, int):
            raise TypeError(f"Expected int for '{self.name}', got {type(self.value).__name__}")

        digit_count = len(str(abs(self.value)))
        if digit_count > BKNumber.MAX_DIGITS:
            raise ValueError(f"Field '{self.name}' exceeds {BKNumber.MAX_DIGITS} digits")

        if self.min_value is not None and self.value < self.min_value:
            raise ValueError(f"Field '{self.name}' is less than minimum value {self.min_value}")

        if self.max_value is not None and self.value > self.max_value:
            raise ValueError(f"Field '{self.name}' is greater than maximum value {self.max_value}")

    def clone_with_value(self, value):
        """Devuelve una copia de sí misma con value distinto (sin mutar la plantilla)."""
        clone = copy.copy(self)
        clone.value = value
        clone.validate_init()       # valida el nuevo valor
        return clone

    def __str__(self):
        return str(self.value) if self.value is not None else "None"


class BKFloat:
    MAX_PRECISION = 38

    def __init__(self
                 , name: str
                 , value=None
                 , precision: int = MAX_PRECISION
                 , scale: int = None
                 , nullable: bool = True
                 , primary_key: bool = False
                 , min_value: float = None
                 , max_value: float = None
                 , doc: str = None):
        self.name = name
        self.value = value
        self.precision = precision
        self.scale = scale
        self.nullable = nullable
        self.primary_key = primary_key
        self.min_value = min_value
        self.max_value = max_value
        self.doc = doc

        self.validate_init()

    def validate_init(self):
        self.__validate_value()

    def __validate_value(self):
        if self.value is None:
            if not self.nullable:
                raise ValueError(f"Field '{self.name}' cannot be null")
            return

        try:
            dec_value = Decimal(str(self.value))
        except (InvalidOperation, ValueError):
            raise TypeError(f"Value for '{self.name}' must be numeric")

        digits = dec_value.as_tuple().digits
        total_digits = len(digits)

        if self.scale is not None:
            # Redondear según escala
            fmt = Decimal(f'1.{"0" * self.scale}')
            dec_value = dec_value.quantize(fmt, rounding=ROUND_HALF_UP)
            decimal_digits = abs(dec_value.as_tuple().exponent)
        else:
            decimal_digits = abs(dec_value.as_tuple().exponent)

        integer_digits = total_digits - decimal_digits
        if total_digits > self.precision:
            raise ValueError(f"Total digits in '{self.name}' exceed {self.precision}")

        if self.min_value is not None and dec_value < Decimal(str(self.min_value)):
            raise ValueError(f"Value for '{self.name}' is less than minimum {self.min_value}")

        if self.max_value is not None and dec_value > Decimal(str(self.max_value)):
            raise ValueError(f"Value for '{self.name}' exceeds maximum {self.max_value}")

        self.value = float(dec_value)

    def clone_with_value(self, value):
        """Devuelve una copia de sí misma con value distinto (sin mutar la plantilla)."""
        clone = copy.copy(self)
        clone.value = value
        clone.validate_init()       # valida el nuevo valor
        return clone

    def __str__(self):
        return str(self.value) if self.value is not None else "None"


class BKDate:
    def __init__(self
                 , name: str
                 , value=None
                 , nullable: bool = True
                 , primary_key: bool = False
                 , doc: str = None):
        self.name = name
        self.value = value
        self.nullable = nullable
        self.primary_key = primary_key
        self.doc = doc

        self.validate_init()

    def validate_init(self):
        self.__validate_value()

    def __validate_value(self):
        if self.value is None:
            if not self.nullable:
                raise ValueError(f"Field '{self.name}' cannot be null")
        elif not isinstance(self.value, date):
            raise TypeError(f"Field '{self.name}' must be a date object")

    def clone_with_value(self, value):
        """Devuelve una copia de sí misma con value distinto (sin mutar la plantilla)."""
        clone = copy.copy(self)
        clone.value = value
        clone.validate_init()       # valida el nuevo valor
        return clone

    def __str__(self):
        return str(self.value) if self.value is not None else "None"


class BKDatetime:
    def __init__(self
                 , name: str
                 , value=None
                 , nullable: bool = True
                 , primary_key: bool = False
                 , doc: str = None):
        self.name = name
        self.value = value
        self.nullable = nullable
        self.primary_key = primary_key
        self.doc = doc

        self.validate_init()

    def validate_init(self):
        self.__validate_value()

    def __validate_value(self):
        if self.value is None:
            if not self.nullable:
                raise ValueError(f"Field '{self.name}' cannot be null")
        elif not isinstance(self.value, datetime):
            raise TypeError(f"Field '{self.name}' must be a datetime object")

    def clone_with_value(self, value):
        """Devuelve una copia de sí misma con value distinto (sin mutar la plantilla)."""
        clone = copy.copy(self)
        clone.value = value
        clone.validate_init()       # valida el nuevo valor
        return clone

    def __str__(self):
        return str(self.value) if self.value is not None else "None"


class BKBytes:
    MAX_BYTES = 2000  # RAW hasta 2000 bytes en Oracle, BLOB hasta 4 GB

    def __init__(self, name: str
                 , value=None
                 , max_bytes: int = MAX_BYTES
                 , nullable: bool = True
                 , primary_key: bool = False
                 , doc: str = None):
        self.name = name
        self.value = value
        self.max_bytes = max_bytes
        self.nullable = nullable
        self.primary_key = primary_key
        self.doc = doc

        self.validate_init()

    def validate_init(self):
        self.__validate_value()

    def __validate_value(self):
        if self.value is None:
            if not self.nullable:
                raise ValueError(f"Field '{self.name}' cannot be null")
        elif not isinstance(self.value, (bytes, bytearray)):
            raise TypeError(f"Field '{self.name}' must be bytes or bytearray")
        elif len(self.value) > self.max_bytes:
            raise ValueError(f"Field '{self.name}' exceeds max size of {self.max_bytes} bytes")

    def clone_with_value(self, value):
        """Devuelve una copia de sí misma con value distinto (sin mutar la plantilla)."""
        clone = copy.copy(self)
        clone.value = value
        clone.validate_init()       # valida el nuevo valor
        return clone

    def __str__(self):
        return str(self.value) if self.value is not None else "None"
