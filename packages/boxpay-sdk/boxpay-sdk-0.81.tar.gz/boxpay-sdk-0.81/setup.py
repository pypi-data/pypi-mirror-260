# setup.py
from setuptools import setup, find_packages

setup(
    name='boxpay-sdk',
    version='0.81',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pydantic',
        'typing',
        'dataclasses'
    ],
)
