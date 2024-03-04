from setuptools import setup, find_packages



setup(
    name='easymerge',
    description='A simple Python library for merging dataframes accommodating variations in language, spelling, and typos. ',
    author='Ethan Mai',
    author_email='iam.ethanmai@gmail.com',
    version='0.3',
    packages=find_packages(),
    install_requires=[
        'python-Levenshtein',
        'pandas',
        'fuzzywuzzy'
    ]
)

