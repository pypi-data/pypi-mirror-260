from setuptools import setup, find_packages


# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name='easymerge',
    description='A simple Python library for merging dataframes accommodating variations in language, spelling, and typos. ',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ethan Mai',
    author_email='iam.ethanmai@gmail.com',
    version='0.4',
    packages=find_packages(),
    install_requires=[
        'python-Levenshtein',
        'pandas',
        'fuzzywuzzy'
    ]
)

