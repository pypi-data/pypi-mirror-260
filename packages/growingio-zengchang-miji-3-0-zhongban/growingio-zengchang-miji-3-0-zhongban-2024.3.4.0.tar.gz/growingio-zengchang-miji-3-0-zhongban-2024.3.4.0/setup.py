#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import GrowingioZengchangMiji30Zhongban
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('GrowingioZengchangMiji30Zhongban'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="growingio-zengchang-miji-3-0-zhongban",
    version=GrowingioZengchangMiji30Zhongban.__version__,
    url="https://github.com/apachecn/growingio-zengchang-miji-3-0-zhongban",
    author=GrowingioZengchangMiji30Zhongban.__author__,
    author_email=GrowingioZengchangMiji30Zhongban.__email__,
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
    description="GrowingIO 增长秘籍 3.0 终版",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "growingio-zengchang-miji-3-0-zhongban=GrowingioZengchangMiji30Zhongban.__main__:main",
            "GrowingioZengchangMiji30Zhongban=GrowingioZengchangMiji30Zhongban.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
