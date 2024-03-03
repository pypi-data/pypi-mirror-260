from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='easymerge',
    description='A simple Python library for merging dataframes accommodating variations in language, spelling, and typos. ',
    author='Ethan Mai',
    author_email='iam.ethanmai@gmail.com',
    version='0.2',
    packages=find_packages(),
    install_requires=requirements
)

