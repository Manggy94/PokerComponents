import os
from dotenv import load_dotenv

load_dotenv()

BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
DATA_DIR = os.getenv("DATA_DIR")
TEST_DATA_DIR = os.getenv("TEST_DATA_DIR")