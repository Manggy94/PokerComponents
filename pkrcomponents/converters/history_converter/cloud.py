import boto3

from pkrcomponents.components.tables.table import Table
from pkrcomponents.converters.history_converter.abstract import AbstractHandHistoryConverter


class CloudHandHistoryConverter(AbstractHandHistoryConverter):
    def __init__(self, bucket_name: str):
        self.s3 = boto3.client("s3")
        self.bucket_name = bucket_name
        self.parsed_prefix = "data/histories/parsed"
        self.table = Table()
        
    def list_parsed_histories_keys(self) -> list:
        paginator = self.s3.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=self.bucket_name, Prefix=self.parsed_prefix)
        keys = [obj["Key"] for page in pages for obj in page.get("Contents", [])]
        return keys
    
    def read_data_text(self, parsed_key: str) -> str:
        response = self.s3.get_object(Bucket=self.bucket_name, Key=parsed_key)
        content = response["Body"].read().decode("utf-8")
        return content
    
    def send_to_corrections(self, file_key: str):
        correction_key = file_key.replace("data", "corrections")
        print(f"Moving {file_key} to {correction_key}")
        self.s3.copy_object(Bucket=self.bucket_name, CopySource=f"{self.bucket_name}/{file_key}",
                            Key=correction_key)
        self.s3.delete_object(Bucket=self.bucket_name, Key=file_key)
        print("Corrupt history files have been moved to corrections directory")

