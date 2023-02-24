
import boto3 
from decouple import config
from sqlalchemy import create_engine

DATABASE_TYPE = 'postgresql'
DBAPI = 'psycopg2'
ENDPOINT = 'database-1.c0lrvxe9frij.eu-west-2.rds.amazonaws.com' # Change it to your AWS endpoint
USER = 'postgres'
PASSWORD = config('DATABASE_PASSWORD')
PORT = 5432
DATABASE = 'postgres'
engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}")


s3_client = boto3.client('s3')
s3 = boto3.resource('s3')

response = s3_client.upload_file('Player.csv', 'unitedplayerdata', 'player_data')

my_bucket = s3.Bucket('unitedplayerdata')

for file in my_bucket.objects.all():
    print(file.key)

