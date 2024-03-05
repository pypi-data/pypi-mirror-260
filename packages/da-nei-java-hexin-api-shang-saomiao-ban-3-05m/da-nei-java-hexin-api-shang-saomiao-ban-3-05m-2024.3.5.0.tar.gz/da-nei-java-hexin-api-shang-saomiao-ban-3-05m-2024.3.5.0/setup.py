#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import DaNeiJavaHexinApiShangSaomiaoBan305m
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('DaNeiJavaHexinApiShangSaomiaoBan305m'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="da-nei-java-hexin-api-shang-saomiao-ban-3-05m",
    version=DaNeiJavaHexinApiShangSaomiaoBan305m.__version__,
    url="https://github.com/apachecn/da-nei-java-hexin-api-shang-saomiao-ban-3-05m",
    author=DaNeiJavaHexinApiShangSaomiaoBan305m.__author__,
    author_email=DaNeiJavaHexinApiShangSaomiaoBan305m.__email__,
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
    description="达内 Java 核心 API（上）_扫描版_3.05M",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "da-nei-java-hexin-api-shang-saomiao-ban-3-05m=DaNeiJavaHexinApiShangSaomiaoBan305m.__main__:main",
            "DaNeiJavaHexinApiShangSaomiaoBan305m=DaNeiJavaHexinApiShangSaomiaoBan305m.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
