from dotenv import load_dotenv
import os

load_dotenv()

ES_HOST = os.getenv('ES_HOST')
ES_PORT = os.getenv('ES_PORT')
ES_USERNAME = os.getenv('ES_USERNAME')
ES_PASSWORD = os.getenv('ES_PASSWORD')
ES_INDEX = os.getenv('ES_INDEX')

DESTINATION_ES_HOST = os.getenv('DESTINATION_ES_HOST')
DESTINATION_ES_PORT = os.getenv('DESTINATION_ES_PORT')
DESTINATION_ES_INDEX = os.getenv('DESTINATION_ES_INDEX')

MINIO_HOST = os.getenv('MINIO_HOST')
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY')
MINIO_BUCKET_NAME = os.getenv('MINIO_BUCKET_NAME')
