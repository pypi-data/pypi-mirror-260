#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import DaNeiJavaShujukuBianchengSaomiaoBan21m
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('DaNeiJavaShujukuBianchengSaomiaoBan21m'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="da-nei-java-shujuku-biancheng-saomiao-ban-2-1m",
    version=DaNeiJavaShujukuBianchengSaomiaoBan21m.__version__,
    url="https://github.com/apachecn/da-nei-java-shujuku-biancheng-saomiao-ban-2-1m",
    author=DaNeiJavaShujukuBianchengSaomiaoBan21m.__author__,
    author_email=DaNeiJavaShujukuBianchengSaomiaoBan21m.__email__,
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
    description="达内 Java 数据库编程_扫描版_2.1M",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "da-nei-java-shujuku-biancheng-saomiao-ban-2-1m=DaNeiJavaShujukuBianchengSaomiaoBan21m.__main__:main",
            "DaNeiJavaShujukuBianchengSaomiaoBan21m=DaNeiJavaShujukuBianchengSaomiaoBan21m.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
