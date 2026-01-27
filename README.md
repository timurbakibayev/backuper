# PostgreSQL to S3 Backup Tool

Backs up multiple PostgreSQL databases to S3-compatible storage.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create `local_config.py` from the example:
   ```bash
   cp local_config_example.py local_config.py
   ```

3. Edit `local_config.py` with your settings:
   ```python
   DATABASES = [
       {
           "name": "my_database",
           "host": "localhost",
           "port": "5432",
           "user": "postgres",
           "password": "password",
       },
       {
           "name": "another_database",
           "host": "db.example.com",
           "port": "5432",
           "user": "admin",
           "password": "secret",
       },
   ]

   S3_CONFIG = {
       "endpoint_url": "https://your-s3-endpoint",
       "access_key_id": "YOUR_ACCESS_KEY",
       "secret_access_key": "YOUR_SECRET_KEY",
       "bucket_name": "your_bucket",
       "region_name": "",  # optional
   }
   ```

## Usage

```bash
./s3_backup.sh
```

Or directly:
```bash
python backup.py
```

Backups are stored as: `{dbname}/{date-time-randint}/db.dump`

Each database gets its own folder in S3. If one database fails, the script continues with the others.

## Crontab

To run daily at 3 AM:
```
0 3 * * * /path/to/backuper/s3_backup.sh
```

## Restore

```bash
pg_restore -h localhost -U postgres -d your_database db.dump
```
