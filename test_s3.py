import os
import boto3
from botocore.client import Config

from local_config import S3_CONFIG

s3 = boto3.client(
    's3',
    endpoint_url=S3_CONFIG['endpoint_url'],
    aws_access_key_id=S3_CONFIG['access_key_id'],
    aws_secret_access_key=S3_CONFIG['secret_access_key'],
    region_name=S3_CONFIG.get('region_name') or 'us-east-1',
    config=Config(signature_version='s3v4'),
)

bucket = S3_CONFIG['bucket_name']

for size_mb in [1, 10, 50, 110]:
    size = size_mb * 1024 * 1024
    data = os.urandom(size)
    key = f'test/size_{size_mb}mb.bin'
    print(f"Uploading {size_mb} MB to {key} ...")
    try:
        s3.put_object(Bucket=bucket, Key=key, Body=data)
        print(f"  OK ({size_mb} MB)")
    except Exception as e:
        print(f"  FAIL ({size_mb} MB): {e}")
