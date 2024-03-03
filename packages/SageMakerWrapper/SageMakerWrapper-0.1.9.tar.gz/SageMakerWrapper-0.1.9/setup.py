from setuptools import setup, find_packages

setup(
    name="SageMakerWrapper",
    version="0.1.9",
    packages=find_packages(),
    install_requires=[
        "sagemaker",
        "boto3",
        "python-dotenv",
    ],
    author="Mattias Kockum",
    author_email="mattias@kockum.net",
    description="A simple wrapper for AWS Sagemaker",
    url="https://github.com/MattiasKockum/SageMakerWrapper",
)
