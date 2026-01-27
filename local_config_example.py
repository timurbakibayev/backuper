DATABASES = [
    {
        "name": "corporoom",
        "host": "localhost",
        "port": "5432",
        "user": "postgres",
        "password": "password",
    },
    {
        "name": "another_db",
        "host": "localhost",
        "port": "5432",
        "user": "postgres",
        "password": "password",
    },
]

S3_CONFIG = {
    "endpoint_url": "https://corporoom.archive.pscloud.io",
    "access_key_id": "YOUR_ACCESS_KEY",
    "secret_access_key": "YOUR_SECRET_KEY",
    "bucket_name": "corporoom",
    "region_name": "",  # optional
}
