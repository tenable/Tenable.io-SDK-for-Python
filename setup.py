from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst')) as file:
    long_description = file.read()

setup(
    name='tenable_io',
    version='0.0',
    description='Tenable.io API SDK',
    long_description=long_description,
    author='Tenable Network Security, Inc',
    packages=find_packages(exclude=['doc', 'tests*']),
    install_requires=[
        "requests>=2.12.1",
        "six>=1.10.0",
    ],
)
