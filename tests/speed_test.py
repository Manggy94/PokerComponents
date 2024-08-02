"""This module tests the time needed to convert a parsed file in local."""

import time
from pkrcomponents.converters.settings import DATA_DIR
from pkrcomponents.converters.history_converter.local import LocalHandHistoryConverter
from pkrcomponents.converters.summary_converter.local import LocalSummaryConverter


def speed_convert_hand_history():
    """Test the time needed to parse a split history file in local."""
    print("Testing parsed hand history conversion time")
    converter = LocalHandHistoryConverter(DATA_DIR)
    last_10_files = converter.list_parsed_histories_keys()[-10:]
    start = time.time()
    for _ in range(10):
        for file_key in last_10_files:
            converter.convert_history(file_key)
    end = time.time()
    total_time = end - start
    average_time = total_time / 100
    print(f"Total time to convert 100 split history files: {total_time:.2f} seconds")
    print(f"Average time to convert a split history file: {average_time:.4f} seconds or "
          f"{average_time * 1000:.1f} milliseconds")


def speed_convert_summary():
    """Test the time needed to parse a summary file in local."""
    print("Testing parsed summary conversion time")
    converter = LocalSummaryConverter(DATA_DIR)
    last_10_files = converter.list_parsed_summaries_keys()[-10:]
    start = time.time()
    for _ in range(10):
        for file_key in last_10_files:
            converter.convert_summary(file_key)
    end = time.time()
    total_time = end - start
    average_time = total_time / 100
    print(f"Total time to convert 100 summary files: {total_time:.2f} seconds")
    print(f"Average time to convert a summary file: {average_time:.4f} seconds or "
          f"{average_time * 1000:.1f} milliseconds")


if __name__ == "__main__":
    speed_convert_hand_history()
    speed_convert_summary()
