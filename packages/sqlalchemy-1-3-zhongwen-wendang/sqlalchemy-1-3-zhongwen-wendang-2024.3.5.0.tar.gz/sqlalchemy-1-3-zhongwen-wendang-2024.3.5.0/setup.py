#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import Sqlalchemy13ZhongwenWendang
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('Sqlalchemy13ZhongwenWendang'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="sqlalchemy-1-3-zhongwen-wendang",
    version=Sqlalchemy13ZhongwenWendang.__version__,
    url="https://github.com/apachecn/sqlalchemy-1-3-zhongwen-wendang",
    author=Sqlalchemy13ZhongwenWendang.__author__,
    author_email=Sqlalchemy13ZhongwenWendang.__email__,
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
    description="SQLAlchemy 1.3 中文文档",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "sqlalchemy-1-3-zhongwen-wendang=Sqlalchemy13ZhongwenWendang.__main__:main",
            "Sqlalchemy13ZhongwenWendang=Sqlalchemy13ZhongwenWendang.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
