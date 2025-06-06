class BKString:
    def __init__(self, name :str
                 , value :str=None
                 , min_lengt :int=0
                 , max_length :int=4000
                 , nullable :bool=True
                 , doc :str=None) -> BkString:
        self.value = value
        self.name = name
        self.max_length = max_length
        self.min_length = min_length
        self.nullable = nullable
        self.doc = doc
    
    def _validate_init(self):
        pass
    
    def __validate_value(self):
        if self.value is not None:
            if not isinstance(self.value, str):
                raise TypeError(f"Expected str, got {type(self.value).__name__}")
            if self.max_length is not None and len(self.value) > self.max_length:
                raise ValueError(f"String length exceeds maximum of {self.max_length}")
            if self.min_length is not None and len(self.value) < self.min_length:
                raise ValueError(f"String length is less than minimum of {self.min_length}")

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
    