#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import NiukeWangMingqiChunzhaoShixiBeizhanGonglveChanpinYunyingPian2019
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('NiukeWangMingqiChunzhaoShixiBeizhanGonglveChanpinYunyingPian2019'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="niuke-wang-mingqi-chunzhao-shixi-beizhan-gonglve-chanpin-yunying-pian-2019",
    version=NiukeWangMingqiChunzhaoShixiBeizhanGonglveChanpinYunyingPian2019.__version__,
    url="https://github.com/apachecn/niuke-wang-mingqi-chunzhao-shixi-beizhan-gonglve-chanpin-yunying-pian-2019",
    author=NiukeWangMingqiChunzhaoShixiBeizhanGonglveChanpinYunyingPian2019.__author__,
    author_email=NiukeWangMingqiChunzhaoShixiBeizhanGonglveChanpinYunyingPian2019.__email__,
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
    description="牛客网名企春招实习备战攻略 产品运营篇 2019",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "niuke-wang-mingqi-chunzhao-shixi-beizhan-gonglve-chanpin-yunying-pian-2019=NiukeWangMingqiChunzhaoShixiBeizhanGonglveChanpinYunyingPian2019.__main__:main",
            "NiukeWangMingqiChunzhaoShixiBeizhanGonglveChanpinYunyingPian2019=NiukeWangMingqiChunzhaoShixiBeizhanGonglveChanpinYunyingPian2019.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
