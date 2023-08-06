import boto3
import uuid

s3_client = boto3.client('s3')

s3_bucket = "debate-app-data"

def generate_s3_key(folder_name, created_date, user_id):
    return f"{folder_name}/{created_date}_{user_id}_{uuid.uuid4()}.txt"