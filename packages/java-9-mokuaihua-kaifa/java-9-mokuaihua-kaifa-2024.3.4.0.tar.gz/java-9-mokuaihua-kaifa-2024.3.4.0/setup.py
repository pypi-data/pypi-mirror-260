#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import Java9MokuaihuaKaifa
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('Java9MokuaihuaKaifa'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="java-9-mokuaihua-kaifa",
    version=Java9MokuaihuaKaifa.__version__,
    url="https://github.com/apachecn/java-9-mokuaihua-kaifa",
    author=Java9MokuaihuaKaifa.__author__,
    author_email=Java9MokuaihuaKaifa.__email__,
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
    description="Java 9 模块化开发",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "java-9-mokuaihua-kaifa=Java9MokuaihuaKaifa.__main__:main",
            "Java9MokuaihuaKaifa=Java9MokuaihuaKaifa.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
