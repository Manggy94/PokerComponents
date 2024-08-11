import os
from pkrcomponents.converters.summary_converter.local import LocalSummaryConverter
from pkrcomponents.converters.settings import DATA_DIR


if __name__ == "__main__":
    converter = LocalSummaryConverter(data_dir=DATA_DIR)
    converter.convert_summaries()
