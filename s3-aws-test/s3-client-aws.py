""" A python script for accessing AWS s3"""

from boto3.session import Session
import uuid
from io import BytesIO

AWS_ACCESS_KEY_ID = "ASIASTWFX7VYDGXDFHIK"
AWS_SECRET_ACCESS_KEY = "YHJsf+wd80iTgX2onz8Y9DJhY//gF+aKWhi/Kg1k"
AWS_SESSION_TOKEN = "FwoGZXIvYXdzEBkaDJCGCat+gaw8xb4yRiLZAf1XzE6N3DTVlowYguWloa69kvRPhhEUSbrVf/LFyiccINU3J4t8XKyoKbw/orkOgo5iFmG82eK1luVr/GuXW/BRAQyuPWtog5pJASDEtisiucOBVrsShm0WUlRbXKt1RXAYqCXIlFU3NCqzXhlf8afvuuBcGfi7hMuhyhwOVndKk7pw/vDcQN+xKpPBWLk4g240XRskSFFHCSclXOiQcL91OY5CLWat/HlGgP0ivKevedDDGqf7D2c48D/PhNG0y0exFv6fGAsjJafmzKrfQ11vW4edZwNk9cIo1Z7GhgYyM/r1CiqrDb5+DpzZeooleSUqQs0pClElVBPd17zFyef+igOdGhewhL3JXmap8gOXrTVm2Q=="
REGION = "eu-central-1"

BUCKET_NAME = "g-s3-py-buck"
REGION = "eu-central-1"


class S3client:
    def __init__(self, secret_key, access_key):
        self.secret_key = secret_key
        self.access_key = access_key
        return

    def create_session(self):
        # Per https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html
        session = Session(aws_access_key_id=AWS_ACCESS_KEY_ID,
                       aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                       aws_session_token=AWS_SESSION_TOKEN,
                       region_name=REGION)
        self.s3 = session.resource('s3')
        self.s3cl = session.client('s3')

    def bucket_create(self, bucket_name):
        try:
            print("Creating a bucket named {}".format(bucket_name))
            self.s3.create_bucket(Bucket=bucket_name,
                                  CreateBucketConfiguration={'LocationConstraint': REGION})
            self.bucket = self.s3.Bucket(bucket_name)
            print("bucket {} created.".format(bucket_name))
            return 0
        except Exception as e:
            print("Error in bucket creation: {}".format(e))
            return 1

    def list_buckets(self):
        buck_list = self.s3cl.list_buckets()
        print('Existing buckets:')
        for bucket in buck_list['Buckets']:
            print(f'  {bucket["Name"]}')

    def bucket_put_object(self, bucket_name, key, body):
        self.bucket.put_object(Bucket=bucket_name, Key=key, Body=body)
        return

    def bucket_download_fileobj(self, key):
        rdata = BytesIO()
        self.bucket.download_fileobj(Fileobj=rdata, Key=key)
        return rdata.getvalue()

    def bucket_clean(self, bucket_name):
        response = self.s3cl.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            for item in response['Contents']:
                print("will delete an object in : {}".format(item['Key']))
                self.s3cl.delete_object(Bucket=bucket_name, Key=item['Key'])
        else:
            print("no content to delete")

        return

    def bucket_delete(self, bucket_name):
        try:
            self.bucket = self.s3.Bucket(bucket_name)
            self.bucket.delete()
            print("bucket {} deleted.".format(bucket_name))
        except Exception as e:
            print("Error in {} bucket deletion: {}".format(bucket_name, e))
        return


if __name__ == "__main__":

    s3client = S3client(secret_key=AWS_SECRET_ACCESS_KEY, access_key=AWS_ACCESS_KEY_ID)

    s3client.create_session()
    # s3client.bucket_delete(BUCKET_NAME)  # needed just in my test
    create = s3client.bucket_create(BUCKET_NAME)
    if create != 0:
        exit(1)

    data_key = "test_key"
    data_body = str(uuid.uuid4())
    print("written str: {}".format(data_body))
    s3client.bucket_put_object(BUCKET_NAME, data_key, data_body)
    read_str = s3client.bucket_download_fileobj(data_key).decode("utf-8")  # decode needed for python 3.8!
    print("read_str: {}".format(read_str))
    s3client.bucket_clean(BUCKET_NAME)
    s3client.list_buckets()
    s3client.bucket_delete(BUCKET_NAME)
