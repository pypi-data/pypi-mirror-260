#!/usr/bin/env python3

import setuptools
from setuptools import find_packages

__ver__ = "1.0.11"
long_description=open('README.md').read()

install_requires = [
        "humanize",
        "numpy",
        "pillow",
        "pytesseract"]

setuptools.setup(
    name="pymates",
    
    author="Matt Harris",
 
    
    author_email="WorkMatthewJHarris94@gmail.com",
    version=__ver__,
    packages=find_packages(
        where='src',
    ),
    package_dir={"": "src"},

    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'mates = pymates.main:run',
            'testmates = pymates.tests:tests',
        ],
    },
    package_data={
      "pymates": ['*.png', '*.mp3', "./tests/*.png"],
    },
    include_package_data=True,
    include_dirs = ["./src/pymates/tests/"],
    
    license="MIT",
    
    long_description=long_description,
    long_description_content_type="text/markdown",

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    )
