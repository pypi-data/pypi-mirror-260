import os
import boto3

import yaml
import tarfile

import sagemaker

def create_tar_gz(folder_path, output_filename):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(folder_path, arcname=".")

# TODO make folders

def upload_data(config_dir="config", data_dir="data"):
    with open(f"{config_dir}/config.yaml", 'r') as file:
        config = yaml.safe_load(file)
    prefix = config["prefix"]
    sess = sagemaker.Session()
    bucket = sess.default_bucket()
    s3 = boto3.resource("s3")
    s3.Bucket(bucket).upload_file(f"{data_dir}/testing/data.tar.gz", f"{prefix}/data/testing/data.tar.gz")
    s3.Bucket(bucket).upload_file(f"{data_dir}/training/data.tar.gz", f"{prefix}/data/training/data.tar.gz")
