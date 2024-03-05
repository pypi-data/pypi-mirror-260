#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import SpringDataJdbc105ReleaseZhongwenWendang
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('SpringDataJdbc105ReleaseZhongwenWendang'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="spring-data-jdbc-1-0-5-release-zhongwen-wendang",
    version=SpringDataJdbc105ReleaseZhongwenWendang.__version__,
    url="https://github.com/apachecn/spring-data-jdbc-1-0-5-release-zhongwen-wendang",
    author=SpringDataJdbc105ReleaseZhongwenWendang.__author__,
    author_email=SpringDataJdbc105ReleaseZhongwenWendang.__email__,
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
    description="Spring Data JDBC 1.0.5.RELEASE 中文文档",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "spring-data-jdbc-1-0-5-release-zhongwen-wendang=SpringDataJdbc105ReleaseZhongwenWendang.__main__:main",
            "SpringDataJdbc105ReleaseZhongwenWendang=SpringDataJdbc105ReleaseZhongwenWendang.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
