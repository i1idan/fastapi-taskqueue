"""define celery tasks"""

from celery.schedules import crontab
from .celery_app import celery
from .config import Config
from datetime import datetime
import boto3
import logging
from pathlib import Path    
import shutil

@celery.task(name="upload_attachment_to_s3")
def upload_attachment_to_s3(file_path:str):
    try:
        s3_resource = boto3.resource('s3',
                                    endpoint_url=Config.S3_ENDPOINT_URL,
                                    aws_access_key_id=Config.S3_ACCESS_KEY_ID,
                                    aws_secret_access_key=Config.S3_SECRET_ACCESS_KEY)

        bucket = s3_resource.Bucket(Config.S3_BUCKET)

        with open(file_path, "rb") as file:
            bucket.put_object(
                ACL='private',
                Body=file,
                Key=f'{datetime.now()}/{Path(file_path).name}')

    except Exception as e:
        logging.error(e)
        return {'status': '400', 'message': f'upload failed due to {e}'}

    return {'status': '200', 'message':'file uploaded successfully'}


@celery.task(name="clean_shared_volume")
def clean_shared_volume(dir_path:str):
    shutil.rmtree(dir_path)
    
