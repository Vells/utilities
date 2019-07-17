"""
Simple script that looks for files starting with
a caller-specified prefix in all available S3 buckets;

Credentials are expected to be found in a configuration file
stored in the home directory of the caller.
details: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html
"""
import logging

import boto3
import botocore
import click

# disable warning caused by use of click
# pylint: disable=no-value-for-parameter


logging.basicConfig(level=logging.INFO)


@click.command()
@click.option('--prefix', '-p', default="", help='S3 prefix')
def find_files(prefix):
    client = boto3.client('s3')
    buckets = client.list_buckets().get("Buckets")
    s3_resource = boto3.resource('s3')

    for bucket_info in buckets:
        bucket_name = bucket_info.get('Name')
        logging.info("bucket: %s", bucket_name)

        try:
            bucket = s3_resource.Bucket(name=bucket_name)
            for obj in bucket.objects.filter(Prefix=prefix):
                logging.info("\t%s: %s", obj.bucket_name, obj.key)
        except botocore.exceptions.ClientError:
            logging.error("Client error!")

def start():
    return find_files(obj={})


if __name__ == "__main__":
    start()
