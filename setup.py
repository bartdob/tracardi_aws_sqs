from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='tracardi-aws-sqs-connector',
    version='0.1',
    description='plugin to send a message to a Amazon AWS SQS queue',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Bart Dobrosielski',
    author_email='bdobrosielski@edu.cdv.pl',
    packages=['tracardi_aws_sqs'],
    install_requires=[
        'tracardi-plugin-sdk>=0.6.21',
        'tracardi>=0.6.18,<=0.7.0',
        'botocore',
        'aiobotocore'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    keywords=['tracardi', 'plugin'],
    include_package_data=True,
    python_requires=">=3.8",
)