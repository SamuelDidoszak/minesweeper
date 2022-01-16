class EmptyValuesException(Exception):
    """
    Exception thrown when not all values were input by the user
    """
    def __init__(self):
        super().__init__("insert all values")
        
class ValuesOutOfBoundsException(Exception):
    """
    Exception thrown when any value input by the user was out of bounds
    """
    def __init__(self, val):
        self.val = val
        super().__init__("{} value is out of bounds".format(val))