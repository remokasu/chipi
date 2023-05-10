from setuptools import find_packages, setup
from codecs import open

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

with open('LICENSE', 'r', encoding='utf-8') as f:
    license = f.read()


setup(
    author='remokasu',
    name="chipi",
    version="0.0.1",
    license=license,
    url='https://github.com/remokasu/chipi',
    packages=find_packages(),
    description='buffer management tool for Python',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
