import os
from dotenv import load_dotenv

load_dotenv()

BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
LOCAL_DATA_DIR = os.getenv("LOCAL_DATA_DIR")
TEST_DATA_DIR = os.getenv("TEST_DATA_DIR")