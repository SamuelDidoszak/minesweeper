class EmptyValuesException(Exception):
    def __init__(self):
        super().__init__("insert all values")
        
class ValuesOutOfBoundsException(Exception):
    def __init__(self, val):
        self.val = val
        super().__init__("{} value is out of bounds".format(val))