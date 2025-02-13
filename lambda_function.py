import boto3
import csv

S3_BUCKET = "alludosunny123"
FILE_NAME = "s3_bucket_list.csv"

def list_s3_buckets():
    s3 = boto3.client("s3", region_name="us-east-1")
    response = s3.list_buckets()
    
    bucket_names = [bucket["Name"] for bucket in response["Buckets"]]

    return bucket_names

def save_to_s3(bucket_list):
    local_file = "/tmp/" + FILE_NAME

    # Write to CSV
    with open(local_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Bucket Name"])
        for bucket in bucket_list:
            writer.writerow([bucket])

    # Upload to S3
    s3_client = boto3.client("s3")
    s3_client.upload_file(local_file, S3_BUCKET, FILE_NAME)

def lambda_handler(event, context):
    buckets = list_s3_buckets()
    save_to_s3(buckets)
    return {"statusCode": 200, "body": f"Bucket list saved to {S3_BUCKET}/{FILE_NAME}"}
