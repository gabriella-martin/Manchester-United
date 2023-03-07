
import boto3 

# push files to s3 bucket

s3_client = boto3.client('s3')
s3 = boto3.resource('s3')

response = s3_client.upload_file('Players.csv', 'football-data-pl', 'player_data')
response = s3_client.upload_file('Fixtures.csv', 'football-data-pl', 'fixture_data')

my_bucket = s3.Bucket('football-data-pl')

# check files have been pushed successfully 

for file in my_bucket.objects.all():
    print(file.key)

