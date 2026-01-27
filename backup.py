import subprocess
import random
from datetime import datetime

import boto3
from botocore.client import Config

from local_config import DATABASES, S3_CONFIG


def get_s3_client():
    return boto3.client(
        's3',
        endpoint_url=S3_CONFIG['endpoint_url'],
        aws_access_key_id=S3_CONFIG['access_key_id'],
        aws_secret_access_key=S3_CONFIG['secret_access_key'],
        region_name=S3_CONFIG.get('region_name') or 'us-east-1',
        config=Config(signature_version='s3v4')
    )


def create_pg_dump(db_config: dict) -> bytes:
    """Run pg_dump and return compressed bytes."""
    import os
    env = os.environ.copy()
    env['PGPASSWORD'] = db_config['password']

    cmd = [
        'pg_dump',
        '-h', db_config['host'],
        '-p', db_config['port'],
        '-U', db_config['user'],
        '-Fc',  # custom format (already compressed, restorable with pg_restore)
        db_config['name']
    ]

    print(f"Running pg_dump for database: {db_config['name']}")
    result = subprocess.run(cmd, env=env, capture_output=True)

    if result.returncode != 0:
        raise Exception(f"pg_dump failed: {result.stderr.decode()}")

    return result.stdout


def upload_to_s3(s3_client, data: bytes, key: str):
    """Upload data to S3."""
    bucket = S3_CONFIG['bucket_name']
    s3_client.put_object(Bucket=bucket, Key=key, Body=data)
    print(f"Uploaded to s3://{bucket}/{key}")


def backup_database(s3_client, db_config: dict):
    """Backup a single database."""
    db_name = db_config['name']
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    rand_suffix = random.randint(100, 999)

    s3_key = f"{db_name}/{timestamp}-{rand_suffix}/db.dump"

    print(f"Starting backup: {s3_key}")

    dump_data = create_pg_dump(db_config)
    print(f"Dump size: {len(dump_data) / 1024 / 1024:.2f} MB")

    upload_to_s3(s3_client, dump_data, s3_key)
    print(f"Backup completed for {db_name}!")


def main():
    s3_client = get_s3_client()

    for db_config in DATABASES:
        try:
            backup_database(s3_client, db_config)
        except Exception as e:
            print(f"Error backing up {db_config['name']}: {e}")
            continue

    print("All backups completed!")


if __name__ == '__main__':
    main()
