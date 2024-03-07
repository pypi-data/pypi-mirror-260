import logging
import os

from setuptools import setup, find_namespace_packages

logger = logging.getLogger(__name__)
VERSION = "0.0.27"
logging.info(f"building version: {VERSION}")

setup(
    name='tgedr-dataops',
    version=VERSION,
    description='data operations related code',
    url='https://github.com/jtviegas-sandbox/dataops',
    author='joao tiago viegas',
    author_email='jtviegas@gmail.com',
    license='Unlicense',
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10'
    ],
    keywords='data engineering mlops ml',
    include_package_data=True,
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    install_requires=[
        "pandas==2.2.0",
        "pyarrow==15.*",
        "s3fs==2024.2.0",
        "boto3==1.34.34"
    ],
    python_requires='>=3.9',
)
