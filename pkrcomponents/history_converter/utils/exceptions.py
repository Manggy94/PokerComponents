class HandConversionError(Exception):
    def __init__(self):
        self.message = "Error converting hand history"
        super().__init__(self.message)