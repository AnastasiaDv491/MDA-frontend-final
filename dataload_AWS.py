import boto3
from dotenv import load_dotenv
import os

class AWS_connector:
    def __init__(self, access_key, secret_key, bucket_name):
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket_name = bucket_name
    def createAWSconnection(self):
        s3 = boto3.resource(
                "s3",
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
            )
        bucket = s3.Bucket(self.bucket_name)
        prefix_objs = bucket.objects.all()

        return prefix_objs

# Get instance of the class that has AWS connection
load_dotenv() #load environment variables
AWS_instantiate = AWS_connector(os.getenv("AWS_ACCESS_KEY"), os.getenv("AWS_SECRET_KEY"), "mda-test")
