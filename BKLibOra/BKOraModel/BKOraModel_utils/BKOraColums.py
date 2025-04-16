class BKOraColumn:
    def __init__(self, name=None, type_=str, default=None, primary_key=False, nullable=True, doc=None):
        self.name = name
        self.type = type_
        self.default = default
        self.primary_key = primary_key
        self.nullable = nullable
        self.doc = doc