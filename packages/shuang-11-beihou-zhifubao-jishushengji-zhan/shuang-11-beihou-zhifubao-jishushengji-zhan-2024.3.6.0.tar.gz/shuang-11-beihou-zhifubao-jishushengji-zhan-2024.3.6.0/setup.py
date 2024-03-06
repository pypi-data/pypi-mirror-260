#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import Shuang11BeihouZhifubaoJishushengjiZhan
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('Shuang11BeihouZhifubaoJishushengjiZhan'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="shuang-11-beihou-zhifubao-jishushengji-zhan",
    version=Shuang11BeihouZhifubaoJishushengjiZhan.__version__,
    url="https://github.com/apachecn/shuang-11-beihou-zhifubao-jishushengji-zhan",
    author=Shuang11BeihouZhifubaoJishushengjiZhan.__author__,
    author_email=Shuang11BeihouZhifubaoJishushengjiZhan.__email__,
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
    description="双 11 背后——支付宝技术升级战",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "shuang-11-beihou-zhifubao-jishushengji-zhan=Shuang11BeihouZhifubaoJishushengjiZhan.__main__:main",
            "Shuang11BeihouZhifubaoJishushengjiZhan=Shuang11BeihouZhifubaoJishushengjiZhan.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
