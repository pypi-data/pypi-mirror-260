import os
import time
from dotenv import load_dotenv
import yaml

from SageMakerWrapper.files_generation import generate_entrypoint

import sagemaker
from sagemaker.pytorch import PyTorch

import boto3

def launch_training(code_dir="code", config_dir="config"):

    load_dotenv()

    with open(f"{config_dir}/config.yaml", 'r') as file:
        config = yaml.safe_load(file)

    with open(f"{config_dir}/train_parameters.yaml", 'r') as file:
        train_parameters = yaml.safe_load(file)

    with open(f"{config_dir}/train_instance.yaml", 'r') as file:
        train_instance_config = yaml.safe_load(file)

    sess = sagemaker.Session()

    role = os.getenv("role")

    prefix = config["prefix"]
    framework_version = config["framework-version"]
    py_version = config["py-version"]

    wait = config["wait"] if "wait" in config else False
    follow = config["follow"] if "follow" in config else True

    bucket = sess.default_bucket()

    output_path = f"s3://{bucket}/{prefix}"

    channels = {
            "training": f"{output_path}/data/training",
            "testing": f"{output_path}/data/testing"
    }

    hyperparameters = generate_entrypoint(code_dir=code_dir, parameters=train_parameters)

    estimator = PyTorch(
        entry_point="entry-point.py",
        source_dir=code_dir,
        role=role,
        framework_version=str(framework_version),
        py_version=str(py_version),
        instance_type=train_instance_config["learning-instance"],
        instance_count=1,
        volume_size=250,
        output_path=f"{output_path}/models",
        hyperparameters=hyperparameters,
        environment={"WANDB_API_KEY": os.getenv("wandb_api_key")}
        )
    estimator.fit(inputs=channels, wait=wait)

    job_name = estimator.latest_training_job.name

    with open('config/save_last_model.yaml', 'w') as file:
        yaml.dump({"last-job-name": job_name}, file)

    print("\nFrom now on the local machine can be disconnected\n")
    print("\nKeep up with the training on Weights&Biases\n")

    while follow and not wait:
        logs = sess.logs_for_job(job_name, wait=True)
        print(logs)
        if 'Training job completed' in logs:
            break
        time.sleep(10)


    download_trained_model = True

    if wait:
        pt_mnist_model_data = estimator.model_data
        if download_trained_model:
            if not os.path.exists("models"):
                os.makedirs("models")
            s3 = boto3.client("s3")
            l = pt_mnist_model_data.split('/')
            key = '/'.join(l[3:])
            dest = "models/" + l[-1]
            s3.download_file(bucket, key, dest)
