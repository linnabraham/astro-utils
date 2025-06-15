#!/bin/env python
from setuptools import setup, find_packages

setup(
    name='astro_utils',
    version='0.1.0',
    author='Linn Abraham',
    author_email='linn.official@gmail.com',
    description='A python package for utility scripts and functions in several astronomy domains',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/linnabraham/astro-utils',  # Update with your repository URL
    packages=find_packages(),  # Automatically finds your package
    license="MIT",
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'scikit-image',
    ],
)
