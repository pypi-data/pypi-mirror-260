from setuptools import setup, find_packages
import os

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='typeboa',
    version='0.1.1',
    description='A simple library for type checking',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Anish Kanthamneni',
    author_email='akneni@gmail.com',
)
