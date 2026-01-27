import os
import subprocess
import gzip
import random
from datetime import datetime
from io import BytesIO

import boto3
from botocore.client import Config


def get_s3_client():
    return boto3.client(
        's3',
        endpoint_url=os.environ['AWS_S3_ENDPOINT_URL'],
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
        region_name=os.environ.get('AWS_S3_REGION_NAME') or 'us-east-1',
        config=Config(signature_version='s3v4')
    )


def create_pg_dump():
    """Run pg_dump and return compressed bytes."""
    env = os.environ.copy()
    env['PGPASSWORD'] = os.environ['DB_PASSWORD']

    cmd = [
        'pg_dump',
        '-h', os.environ['DB_HOST'],
        '-p', os.environ['DB_PORT'],
        '-U', os.environ['DB_USER'],
        '-Fc',  # custom format (already compressed, restorable with pg_restore)
        os.environ['DB_NAME']
    ]

    print(f"Running pg_dump for database: {os.environ['DB_NAME']}")
    result = subprocess.run(cmd, env=env, capture_output=True)

    if result.returncode != 0:
        raise Exception(f"pg_dump failed: {result.stderr.decode()}")

    return result.stdout


def upload_to_s3(s3_client, data: bytes, key: str):
    """Upload data to S3."""
    bucket = os.environ['AWS_STORAGE_BUCKET_NAME']
    s3_client.put_object(Bucket=bucket, Key=key, Body=data)
    print(f"Uploaded to s3://{bucket}/{key}")


def main():
    db_name = os.environ['DB_NAME']
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    rand_suffix = random.randint(100, 999)

    s3_key = f"{db_name}/{timestamp}-{rand_suffix}/db.dump"

    print(f"Starting backup: {s3_key}")

    dump_data = create_pg_dump()
    print(f"Dump size: {len(dump_data) / 1024 / 1024:.2f} MB")

    s3_client = get_s3_client()
    upload_to_s3(s3_client, dump_data, s3_key)

    print("Backup completed successfully!")


if __name__ == '__main__':
    main()
