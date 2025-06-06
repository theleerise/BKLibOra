from BKLibOra.utils import get_byte_size

class BKString:

    MAX_BYTES = 4000
    
    def __init__(self
                 , name :str
                 , value :str=None
                 , large :int=MAX_BYTES
                 , min_length :int=0
                 , nullable :bool=True
                 , doc :str=None
                 , _encoding :str="utf-8"):
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


    def __str__(self):
        return str(self.value) if self.value is not None else "None"

class BKNumber:
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return str(self.value) if self.value is not None else "None"

class BKfloat:
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return str(self.value) if self.value is not None else "None"
    
class BKDate:
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return str(self.value) if self.value is not None else "None"
    
class BKDatetime:
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return str(self.value) if self.value is not None else "None"

class BKBytes:
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return str(self.value) if self.value is not None else "None"
