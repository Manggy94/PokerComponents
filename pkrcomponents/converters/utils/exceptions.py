class HandConversionError(Exception):
    def __init__(self):
        self.message = "Error converting hand history"
        super().__init__(self.message)


class SummaryConversionError(Exception):
    def __init__(self):
        self.message = "Error converting summary"
        super().__init__(self.message)


