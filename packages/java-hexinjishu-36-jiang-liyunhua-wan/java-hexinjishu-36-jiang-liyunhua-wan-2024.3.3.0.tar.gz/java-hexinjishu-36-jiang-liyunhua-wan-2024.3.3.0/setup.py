#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import JavaHexinjishu36JiangLiyunhuaWan
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('JavaHexinjishu36JiangLiyunhuaWan'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="java-hexinjishu-36-jiang-liyunhua-wan",
    version=JavaHexinjishu36JiangLiyunhuaWan.__version__,
    url="https://github.com/apachecn/java-hexinjishu-36-jiang-liyunhua-wan",
    author=JavaHexinjishu36JiangLiyunhuaWan.__author__,
    author_email=JavaHexinjishu36JiangLiyunhuaWan.__email__,
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
    description="Java 核心技术 36 讲（李运华）（完）",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "java-hexinjishu-36-jiang-liyunhua-wan=JavaHexinjishu36JiangLiyunhuaWan.__main__:main",
            "JavaHexinjishu36JiangLiyunhuaWan=JavaHexinjishu36JiangLiyunhuaWan.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
