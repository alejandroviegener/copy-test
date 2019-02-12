"""Muttlib setup file."""
import setuptools

import muttlib

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='muttlib-mutt',
    version=muttlib.__version__,
    author='Mutt Data',
    author_email='pablo@muttdata.ai',
    description='Collection of helper modules by Mutt Data.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'jinja2',
        'pandas',
        'progressbar2',
        'pyarrow',
        'pyyaml',
        'sqlalchemy',
        'scipy',
    ],
    extras_require={
        'oracle': ['cx_Oracle'],
        'hive': ['pyhive'],
        'postgres': ['psycopg2'],
        'sqlserver': ['pymssql'],
        'mongo': ['pymongo'],
        'ibis': ['ibis'],
        'ipynb-utils': [
            'IPython',
            'jinja2',
            'jinjasql',
            'matplotlib',
            'numpy',
            'pandas',
            'seaborn',
            'tabulate',
            'textwrap',
        ],
        'dev': [
            'pre-commit',
            'flake8',
            'flake8-bugbear',
            'flake8-docstrings',
            'black',
            'mypy',
            'pylint',
        ],
    },
)
