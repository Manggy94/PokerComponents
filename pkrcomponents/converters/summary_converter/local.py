import os

from pkrcomponents.components.tournaments.tournament import Tournament
from pkrcomponents.converters.summary_converter.abstract import AbstractSummaryConverter


class LocalSummaryConverter(AbstractSummaryConverter):
    """"""
    def __init__(self, data_dir: str):
        data_dir = self.correct_data_dir(data_dir)
        self.parsed_dir = os.path.join(data_dir, "summaries", "parsed")
        self.tournament = Tournament()

    @staticmethod
    def correct_data_dir(data_dir: str) -> str:
        if not os.path.exists(data_dir):
            data_dir = data_dir.replace("C:/", "/mnt/c/")
        return data_dir

    def list_parsed_summaries_keys(self) -> list:
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

    @staticmethod
    def send_to_corrections(file_key: str):
        correction_key = file_key.replace("data", "corrections")
        os.makedirs(os.path.dirname(correction_key), exist_ok=True)
        print(f"Moving {file_key} to {correction_key}")
        os.replace(file_key, correction_key)
        print("Corrupt summary files have been moved to corrections directory")