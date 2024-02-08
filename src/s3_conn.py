import boto3
from dotenv import load_dotenv, find_dotenv

from botocore.exceptions import ClientError
import json


load_dotenv(find_dotenv())
print("something is happening!")


# Let's use Amazon S3
s3 = boto3.resource('s3')

def printBuckets():
    for bucket in s3.buckets.all():
        print(bucket.name)

def uploadModel(modelFilePath):
    with open(modelFilePath, 'rb') as data:
        s3.Bucket('mov-dev-bucket').put_object(Key='test/test.jpg', Body=data)

################### maintaining ########################

def checkAccessKeys():
    try:
        # Attempt to list buckets, this will trigger an API call
        for bucket in s3.buckets.all():
            print(bucket.name)
        
        print("Access keys are valid!")
    except ClientError as e:
        if e.response['Error']['Code'] == 'InvalidAccessKeyId':
            print("Invalid access key ID provided.")
        elif e.response['Error']['Code'] == 'SignatureDoesNotMatch':
            print("Invalid secret access key provided.")
        else:
            print("An error occurred:", e)

# Call the function to check access keys
#checkAccessKeys()

################## list, get and upload objects #######################

def listObjects(bucket_name):
    try:
        # Get the bucket
        bucket = s3.Bucket(bucket_name)
        bucket_data = []
        # List all objects and folders in the bucket
        print("Objects and folders in the bucket:")
        for obj in bucket.objects.all():
            print(obj.key)
            bucket_data.append( obj.key )
        return bucket_data
    except Exception as e:
        print("An error occurred:", e)

def getObject(bucket_name, object_key):
    try:
        # Get the object from the bucket
        obj = s3.Object(bucket_name, object_key)
        response = obj.get()
        
        # Print the content of the object
        print("Content of the object:")
        print(response['Body'].read().decode('utf-8'))
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            print("The specified object does not exist.")
        else:
            print("An error occurred:", e)

##################### Pre-signed-URL ############################

s3Client = boto3.client('s3')

def generatePresignedUrl(bucket_name, object_key, expiration=3600):
    try:
        # Generate a pre-signed URL for the specified object
        response = s3Client.generate_presigned_url('get_object',
                                             Params={'Bucket': bucket_name, 'Key': object_key},
                                             ExpiresIn=expiration,
                                             )
        return response
    except Exception as e:
        print("An error occurred:", e)




######################################################################

#listObjects('mov-dev-bucket')

#getObject('mov-dev-bucket', '3dup.svg')

#uploadModel("test/test.jpeg")


#s3 = boto3.client('s3')
#s3.download_file('mov-dev-bucket', '3dup.svg', '3dup.svg')
#with open('3dup.svg', 'wb') as f:
#    s3.download_fileobj('mov-dev-bucket', '3dup.svg', f)