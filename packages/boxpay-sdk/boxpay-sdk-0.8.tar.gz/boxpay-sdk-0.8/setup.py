from setuptools import setup

setup(
    name='boxpay-sdk',
    version='0.8',
    py_modules=['sdk_client', 'checkout_client', 'exceptions', 'models'],
    install_requires=[
        'requests',
        'pydantic',
        'typing',
        'dataclasses'
    ],
)