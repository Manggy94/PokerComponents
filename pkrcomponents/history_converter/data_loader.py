import boto3
import os
import json
from pkrcomponents.history_converter.directories import BUCKET_NAME, LOCAL_DATA_DIR


class S3DataLoader:
    def __init__(self, bucket_name: str = BUCKET_NAME):
        self.s3 = boto3.client('s3')
        self.bucket_name = bucket_name
        self.parsed_prefix = "data/histories/parsed"
        self.corrections_prefix = "corrections"

    def get_data(self, file_key: str) -> str:
        response = self.s3.get_object(Bucket=self.bucket_name, Key=file_key)
        content = response['Body'].read().decode('utf-8')
        data = json.loads(content)
        return data

    def get_files_list(self):
        paginator = self.s3.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=self.bucket_name, Prefix=self.parsed_prefix)
        keys = [obj["Key"] for page in pages for obj in page.get("Contents", [])]
        return keys

    @staticmethod
    def get_split_path(file_key: str) -> str:
        return file_key.replace("parsed", "split").replace(".json", ".txt")

    def move_to_correction_dir(self, file_key: str):
        split_path = self.get_split_path(file_key)
        json_correction_path = file_key.replace("data", "corrections")
        split_correction_path = split_path.replace("data", "corrections")
        # Copy the files to the corrections directory
        print(f"Move {file_key} to {json_correction_path}")
        self.s3.copy_object(Bucket=self.bucket_name, CopySource=f"{self.bucket_name}/{file_key}",
                            Key=json_correction_path)
        print(f"Move {split_path} to {split_correction_path}")
        self.s3.copy_object(Bucket=self.bucket_name, CopySource=f"{self.bucket_name}/{split_path}",
                            Key=split_correction_path)
        # Delete the original files
        self.s3.delete_object(Bucket=self.bucket_name, Key=file_key)
        self.s3.delete_object(Bucket=self.bucket_name, Key=split_path)


class LocalDataLoader:
    def __init__(self, data_dir: str = LOCAL_DATA_DIR):
        if not os.path.exists(data_dir):
            data_dir = data_dir.replace("C:/", "/mnt/c/")
        self.data_dir = data_dir
        self.parsed_dir = os.path.join(data_dir, "histories", "parsed")
        self.corrections_dir = data_dir.replace("data", "corrections")

    @staticmethod
    def get_data(file_path: str) -> dict:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    def get_files_list(self):
        return [
            os.path.join(root, filename)
            for root, _, filenames in os.walk(self.data_dir)
            for filename in filenames if filename.endswith('.json')
        ]

    @staticmethod
    def get_split_path(file_path: str) -> str:
        return file_path.replace("parsed", "split").replace(".json", ".txt")

    def move_to_correction_dir(self, file_path: str):
        split_path = self.get_split_path(file_path)
        json_correction_path = file_path.replace("data", "corrections")
        split_correction_path = split_path.replace("data", "corrections")
        # Create correction_directories
        os.makedirs(os.path.dirname(json_correction_path), exist_ok=True)
        print(f"Moving {file_path} to {json_correction_path}")
        os.replace(file_path, json_correction_path)
        os.makedirs(os.path.dirname(split_correction_path), exist_ok=True)
        print(f"Moving {split_path} to {split_correction_path}")
        os.replace(split_path, split_correction_path)
        print("Corrupt history files have been moved to corrections directory")
