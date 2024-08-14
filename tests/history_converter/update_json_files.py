import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
FILES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "json_files")
DATA_DIR = os.getenv("DATA_DIR")
def get_n_parent(path, n):
    """
    Returns the n parent of a path
    """
    for _ in range(n):
        path = os.path.dirname(path)
    return path


def get_origin_file(json_file):
    """
    Returns the origin file of a json example file
    """
    with open(os.path.join(FILES_DIR, json_file), "r") as f:
        data = json.load(f)
    date = datetime.strptime(data["datetime"], "%d-%m-%Y %H:%M:%S").date()
    year, month, day = f"{date.year}", f"{date.month:02}", f"{date.day:02}"
    return os.path.join(
        DATA_DIR, "histories", "parsed", year, month, day,
        data["tournament_info"]["tournament_id"], f"{data['hand_id']}.json"
    )

def replace_with_origin_file(json_file):
    """
    Replaces the json example file with the origin file
    """
    with open(get_origin_file(json_file), "r", encoding="utf-8") as f:
        data = json.load(f)
    with open(os.path.join(FILES_DIR, json_file), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def replace_all_files():
    """
    Replaces all the json example files with the origin files
    """
    for file in os.listdir(FILES_DIR):
        replace_with_origin_file(file)


if __name__ == "__main__":
    replace_all_files()