import os

BUCKET_NAME = os.getenv("POKER_AWS_BUCKET_NAME")
DATA_DIR = os.environ.get("POKER_DATA_DIR")
TEST_DATA_DIR = os.getenv("POKER_TEST_DATA_DIR")