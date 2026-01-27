# PostgreSQL to S3 Backup Tool

Backs up a PostgreSQL database to S3-compatible storage.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set environment variables (see `local.sh` for example):
   ```bash
   export DB_NAME="your_database"
   export DB_USER="postgres"
   export DB_PASSWORD="password"
   export DB_HOST="localhost"
   export DB_PORT=5432
   export AWS_ACCESS_KEY_ID="your_key"
   export AWS_SECRET_ACCESS_KEY="your_secret"
   export AWS_STORAGE_BUCKET_NAME="your_bucket"
   export AWS_S3_ENDPOINT_URL="https://your-s3-endpoint"
   export AWS_S3_REGION_NAME=""
   ```

## Usage

```bash
./s3_backup.sh
```

Or manually:
```bash
source local.sh
python backup.py
```

Backups are stored as: `{dbname}/{date-time-randint}/db.dump`

## Crontab

To run daily at 3 AM:
```
0 3 * * * /Users/timurbakibayev/projects/backuper/s3_backup.sh
```

## Restore

```bash
pg_restore -h localhost -U postgres -d your_database db.dump
```
