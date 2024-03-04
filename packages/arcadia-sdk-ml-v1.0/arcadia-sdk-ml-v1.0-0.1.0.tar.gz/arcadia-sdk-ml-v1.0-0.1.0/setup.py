from setuptools import setup, find_packages

setup(
    name='arcadia-sdk-ml-v1.0',
    version='0.1.0',
    description='Deploy ML Models and Earn via API billing',
    author='Tim Cvetko',
    author_email='cvetko.tim@gmail.com',
    packages=find_packages(),
    install_requires=[
        'requests',  # Example dependency
    ],
)
