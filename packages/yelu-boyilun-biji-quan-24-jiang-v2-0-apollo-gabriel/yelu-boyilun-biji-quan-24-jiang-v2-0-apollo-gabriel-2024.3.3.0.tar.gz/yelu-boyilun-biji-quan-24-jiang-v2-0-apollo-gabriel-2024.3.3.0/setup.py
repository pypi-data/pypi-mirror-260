#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import YeluBoyilunBijiQuan24JiangV20ApolloGabriel
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('YeluBoyilunBijiQuan24JiangV20ApolloGabriel'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="yelu-boyilun-biji-quan-24-jiang-v2-0-apollo-gabriel",
    version=YeluBoyilunBijiQuan24JiangV20ApolloGabriel.__version__,
    url="https://github.com/apachecn/yelu-boyilun-biji-quan-24-jiang-v2-0-apollo-gabriel",
    author=YeluBoyilunBijiQuan24JiangV20ApolloGabriel.__author__,
    author_email=YeluBoyilunBijiQuan24JiangV20ApolloGabriel.__email__,
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
    description="耶鲁博弈论笔记全 24 讲 v2.0（Apollo, Gabriel）",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "yelu-boyilun-biji-quan-24-jiang-v2-0-apollo-gabriel=YeluBoyilunBijiQuan24JiangV20ApolloGabriel.__main__:main",
            "YeluBoyilunBijiQuan24JiangV20ApolloGabriel=YeluBoyilunBijiQuan24JiangV20ApolloGabriel.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
