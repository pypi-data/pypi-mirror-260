#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import YehuoIMxRtKuKaifaShizhanZhinan
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('YehuoIMxRtKuKaifaShizhanZhinan'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="yehuo-i-mx-rt-ku-kaifa-shizhan-zhinan",
    version=YehuoIMxRtKuKaifaShizhanZhinan.__version__,
    url="https://github.com/apachecn/yehuo-i-mx-rt-ku-kaifa-shizhan-zhinan",
    author=YehuoIMxRtKuKaifaShizhanZhinan.__author__,
    author_email=YehuoIMxRtKuKaifaShizhanZhinan.__email__,
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
    description="野火 i.MX RT 库开发实战指南",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "yehuo-i-mx-rt-ku-kaifa-shizhan-zhinan=YehuoIMxRtKuKaifaShizhanZhinan.__main__:main",
            "YehuoIMxRtKuKaifaShizhanZhinan=YehuoIMxRtKuKaifaShizhanZhinan.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
