import os

from pkrcomponents.components.tables.table import Table
from pkrcomponents.converters.history_converter.abstract import AbstractHandHistoryConverter


class LocalHandHistoryConverter(AbstractHandHistoryConverter):
    
    def __init__(self, data_dir: str):
        data_dir = self.correct_data_dir(data_dir)
        self.parsed_dir = os.path.join(data_dir, "histories", "parsed")
        self.table = Table()
        
    @staticmethod
    def correct_data_dir(data_dir: str) -> str:
        if not os.path.exists(data_dir):
            data_dir = data_dir.replace("C:/", "/mnt/c/")
        return data_dir
    
    def list_parsed_histories_keys(self) -> list:
        parsed_keys = [
            os.path.join(root, filename)
            for root, _, filenames in os.walk(self.parsed_dir)
            for filename in filenames if filename.endswith('.json')
        ]
        return parsed_keys
    
    def read_data_text(self, parsed_key: str) -> str:
        with open(parsed_key, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    
    def send_to_corrections(self, file_key: str):
        correction_key = file_key.replace("data", "corrections")
        os.makedirs(os.path.dirname(correction_key), exist_ok=True)
        print(f"Moving {file_key} to {correction_key}")
        os.replace(file_key, correction_key)
        print("Corrupt history files have been moved to corrections directory")
        # Write file_key to a correction file
        # with open(os.path.join(self.data_dir, "parsed_to_correct.txt"), 'w') as file:
        #     file.write(file_key + "\n")