from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

about = {}
exec(open(path.join(here, 'tenable_io/__init__.py')).read(), about)

with open(path.join(here, 'README.rst')) as file:
    long_description = file.read()

setup(
    name='tenable_io',
    version=about['__version__'],
    description='Tenable.io API SDK',
    long_description=long_description,
    author='Tenable Network Security, Inc',
    url='https://github.com/tenable/Tenable.io-SDK-for-Python',
    packages=find_packages(exclude=['doc', 'tests*']),
    license='MIT License',
    install_requires=[
        "requests>=2.12.1",
        "six>=1.10.0",
    ],
)
