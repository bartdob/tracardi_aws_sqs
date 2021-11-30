from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='tracardi-aws-sqs-connector',
    version='0.6.0',
    description='Plugin that sends a message to the Amazon AWS SQS queue',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Bart Dobrosielski, Risto Kowaczewski',
    author_email='bdobrosielski@edu.cdv.pl',
    packages=['tracardi_aws_sqs'],
    install_requires=[
        'tracardi-plugin-sdk>=0.6.29',
        'tracardi>=0.6.21,<=0.7.0',
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