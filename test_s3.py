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

key = 'test/hello.txt'
body = b'hello from test_s3.py\n'

print(f"Uploading to bucket={S3_CONFIG['bucket_name']} key={key} ...")
s3.put_object(Bucket=S3_CONFIG['bucket_name'], Key=key, Body=body)
print("OK")

print("Reading back...")
resp = s3.get_object(Bucket=S3_CONFIG['bucket_name'], Key=key)
print("Content:", resp['Body'].read())
