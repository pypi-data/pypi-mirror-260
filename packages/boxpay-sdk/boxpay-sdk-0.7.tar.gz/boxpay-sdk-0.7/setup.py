# setup.py
from setuptools import setup

setup(
    name='boxpay-sdk',
    version='0.7',  # Update this to the correct version
    py_modules=['boxpay_checkout_sdk'],
    install_requires=[
        'requests',
        'pydantic',
        'typing',
        'dataclasses'
    ],
)
