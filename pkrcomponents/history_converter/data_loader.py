import boto3
import os
import json
from pkrcomponents.history_converter.directories import BUCKET_NAME, LOCAL_DATA_DIR


class S3DataLoader:
    def __init__(self, bucket_name: str = BUCKET_NAME):
        self.s3 = boto3.client('s3')
        self.bucket_name = bucket_name
        self.parsed_prefix = "data/histories/parsed"

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


class LocalDataLoader:
    def __init__(self, data_dir: str = LOCAL_DATA_DIR):
        if not os.path.exists(data_dir):
            data_dir = data_dir.replace("C:/", "/mnt/c/")
        self.data_dir = data_dir
        self.parsed_dir = os.path.join(data_dir, "histories", "parsed")

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
