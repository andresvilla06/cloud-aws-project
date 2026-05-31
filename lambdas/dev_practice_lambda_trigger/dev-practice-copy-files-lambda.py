import boto3
import json
import logging

def get_client_s3(region: str = "us-east-1"):
    """Creates and returns an S3 boto3 client."""
    return boto3.client("s3", region_name=region)

def list_buckets(client) -> list[dict]:
    """ Returns a list of objects inside a bucket under a given prefix."""
    response = client.list_buckets()
    return response.get("Buckets", [])

def list_objets(client, bucket:str, prefix:str = "") -> list[dict]:
    """Returns a list of objects inside a bucket under a given prefix."""
    response = client.list_objects_v2(Bucket=bucket, Prefix=prefix)
    return response.get("Contents", [])

def main() -> None:
    client = get_client_s3()
    buckets = list_buckets(client)
    input_bucket = "dev-practice-raw-234291-s3"

    for bucket in buckets:
        if bucket["Name"] != input_bucket:
            print(bucket["Name"])
            objects = list_objets(client, bucket=bucket["Name"], prefix="data/")
            for obj in objects:
                print(obj["Key"])
            print()
                    
if __name__ == "__main__":
    main()