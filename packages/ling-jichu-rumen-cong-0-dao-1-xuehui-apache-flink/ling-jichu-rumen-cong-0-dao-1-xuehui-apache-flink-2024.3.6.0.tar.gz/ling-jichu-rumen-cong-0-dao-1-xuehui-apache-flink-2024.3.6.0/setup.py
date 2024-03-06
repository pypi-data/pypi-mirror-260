#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import LingJichuRumenCong0Dao1XuehuiApacheFlink
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('LingJichuRumenCong0Dao1XuehuiApacheFlink'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="ling-jichu-rumen-cong-0-dao-1-xuehui-apache-flink",
    version=LingJichuRumenCong0Dao1XuehuiApacheFlink.__version__,
    url="https://github.com/apachecn/ling-jichu-rumen-cong-0-dao-1-xuehui-apache-flink",
    author=LingJichuRumenCong0Dao1XuehuiApacheFlink.__author__,
    author_email=LingJichuRumenCong0Dao1XuehuiApacheFlink.__email__,
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
    description="零基础入门：从0到1学会 Apache Flink",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "ling-jichu-rumen-cong-0-dao-1-xuehui-apache-flink=LingJichuRumenCong0Dao1XuehuiApacheFlink.__main__:main",
            "LingJichuRumenCong0Dao1XuehuiApacheFlink=LingJichuRumenCong0Dao1XuehuiApacheFlink.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
