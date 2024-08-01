import os
from pkrcomponents.converters.history_converter.local import LocalHandHistoryConverter
from pkrcomponents.converters.settings import LOCAL_DATA_DIR


if __name__ == "__main__":
    converter = LocalHandHistoryConverter(data_dir=LOCAL_DATA_DIR)
    converter.parsed_dir = os.path.join(converter.parsed_dir, "2015", "11")
    converter.convert_histories()