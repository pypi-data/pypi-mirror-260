#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import Hibernate54ZhongwenWendang
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('Hibernate54ZhongwenWendang'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="hibernate-5-4-zhongwen-wendang",
    version=Hibernate54ZhongwenWendang.__version__,
    url="https://github.com/apachecn/hibernate-5-4-zhongwen-wendang",
    author=Hibernate54ZhongwenWendang.__author__,
    author_email=Hibernate54ZhongwenWendang.__email__,
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
    description="Hibernate 5.4 中文文档",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "hibernate-5-4-zhongwen-wendang=Hibernate54ZhongwenWendang.__main__:main",
            "Hibernate54ZhongwenWendang=Hibernate54ZhongwenWendang.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
