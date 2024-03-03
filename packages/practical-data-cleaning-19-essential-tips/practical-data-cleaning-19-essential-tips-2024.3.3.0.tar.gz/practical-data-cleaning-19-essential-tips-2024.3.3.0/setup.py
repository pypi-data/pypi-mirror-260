#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import PracticalDataCleaning19EssentialTips
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('PracticalDataCleaning19EssentialTips'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="practical-data-cleaning-19-essential-tips",
    version=PracticalDataCleaning19EssentialTips.__version__,
    url="https://github.com/apachecn/practical-data-cleaning-19-essential-tips",
    author=PracticalDataCleaning19EssentialTips.__author__,
    author_email=PracticalDataCleaning19EssentialTips.__email__,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: Other/Proprietary License",
        "Natural Language :: Chinese (Simplified)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Text Processing :: Markup :: Markdown",
        "Topic :: Text Processing :: Markup :: HTML",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Documentation",
        "Topic :: Documentation",
    ],
    description="Practical Data Cleaning - 19 Essential Tips",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "practical-data-cleaning-19-essential-tips=PracticalDataCleaning19EssentialTips.__main__:main",
            "PracticalDataCleaning19EssentialTips=PracticalDataCleaning19EssentialTips.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
