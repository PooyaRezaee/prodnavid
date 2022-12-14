import boto3
from django.conf import settings


class BucketManager:
    def __init__(self):
        self.connection = boto3.resource('s3',
                                    endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                                    aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID,
                                    aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY,
                                    )

    
    def get_key_object(self):
        pass

    def upload_obj(self,path):
        bucket = self.connection.Bucket('navidbeat')
        file_path = path
        object_name = 'test.txt'

        with open(file_path, "rb") as file:
            bucket.put_object(
                ACL='private',
                Body=file,
                Key=object_name
            )
    
    def download_obj(self):
        bucket = self.connection.Bucket('navidbeat')

        object_name = 'test.txt'
        download_path = './file.txt'

        bucket.download_file(
            object_name,
            download_path
        )
    
    def delete_obj(self,name_file):
        object_name = name_file

        bucket = self.connection.Bucket('navidbeat')
        object = bucket.Object(object_name)

        response = object.delete()

bucket = BucketManager()