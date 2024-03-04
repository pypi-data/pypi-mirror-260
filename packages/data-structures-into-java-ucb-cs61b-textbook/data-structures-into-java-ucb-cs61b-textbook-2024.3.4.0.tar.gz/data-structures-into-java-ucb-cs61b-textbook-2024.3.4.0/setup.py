#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import DataStructuresIntoJavaUcbCs61bTextbook
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('DataStructuresIntoJavaUcbCs61bTextbook'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="data-structures-into-java-ucb-cs61b-textbook",
    version=DataStructuresIntoJavaUcbCs61bTextbook.__version__,
    url="https://github.com/apachecn/data-structures-into-java-ucb-cs61b-textbook",
    author=DataStructuresIntoJavaUcbCs61bTextbook.__author__,
    author_email=DataStructuresIntoJavaUcbCs61bTextbook.__email__,
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
    description="Data Structures Into Java (UCB CS61b textbook)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "data-structures-into-java-ucb-cs61b-textbook=DataStructuresIntoJavaUcbCs61bTextbook.__main__:main",
            "DataStructuresIntoJavaUcbCs61bTextbook=DataStructuresIntoJavaUcbCs61bTextbook.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
