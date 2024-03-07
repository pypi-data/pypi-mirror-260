from setuptools import setup, find_namespace_packages

setup(
  name='snqueue',
  version='0.7.0',
  description='Message-driven req/res implementation using AWS SNS/SQS',
  package_dir={"": "src"},
  packages=find_namespace_packages(where="src"),
  install_requires=[
    "boto3",
    "pycryptodomex",
    "pydantic[email]",
    "pydantic-settings",
    "python-dateutil"
  ]
)