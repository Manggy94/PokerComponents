import os
from pkrcomponents.converters.history_converter.local import LocalHandHistoryConverter
from pkrcomponents.converters.settings import DATA_DIR


if __name__ == "__main__":
    converter = LocalHandHistoryConverter(data_dir=DATA_DIR)
    converter.convert_histories()