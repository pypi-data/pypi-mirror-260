#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import JavaKaifaShouceTaishanBanLinghun13Wen
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('JavaKaifaShouceTaishanBanLinghun13Wen'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="java-kaifa-shouce-taishan-ban-linghun-13-wen",
    version=JavaKaifaShouceTaishanBanLinghun13Wen.__version__,
    url="https://github.com/apachecn/java-kaifa-shouce-taishan-ban-linghun-13-wen",
    author=JavaKaifaShouceTaishanBanLinghun13Wen.__author__,
    author_email=JavaKaifaShouceTaishanBanLinghun13Wen.__email__,
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
    description="〈Java开发手册（泰山版）〉灵魂13问",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "java-kaifa-shouce-taishan-ban-linghun-13-wen=JavaKaifaShouceTaishanBanLinghun13Wen.__main__:main",
            "JavaKaifaShouceTaishanBanLinghun13Wen=JavaKaifaShouceTaishanBanLinghun13Wen.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
