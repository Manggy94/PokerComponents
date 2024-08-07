class HandConversionError(Exception):
    def __init__(self, file_key: str):
        self.message = f"Hand Conversion Error for file {file_key}"
        super().__init__(self.message)


class SummaryConversionError(Exception):
    def __init__(self):
        self.message = "Error converting summary"
        super().__init__(self.message)


