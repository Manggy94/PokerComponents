class HandConversionError(Exception):
    def __init__(self, file_key: str, original_exception: Exception = None):
        self.file_key = file_key
        self.original_exception = original_exception
        if original_exception:
            self.message = (f"Hand Conversion Error for file {file_key}. "
                            f"Original error: {str(original_exception)}")
        else:
            self.message = f"Hand Conversion Error for file {file_key}"
        super().__init__(self.message)


class SummaryConversionError(Exception):
    def __init__(self, original_exception: Exception = None):
        self.original_exception = original_exception
        if original_exception:
            self.message = (f"Error converting summary. "
                            f"Original error: {str(original_exception)}")
        else:
            self.message = "Error converting summary"
        super().__init__(self.message)