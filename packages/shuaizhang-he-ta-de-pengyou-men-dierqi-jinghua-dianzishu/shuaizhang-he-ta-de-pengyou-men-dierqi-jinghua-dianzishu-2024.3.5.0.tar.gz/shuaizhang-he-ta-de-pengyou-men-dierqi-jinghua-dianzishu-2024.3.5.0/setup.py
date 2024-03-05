#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import ShuaizhangHeTaDePengyouMenDierqiJinghuaDianzishu
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('ShuaizhangHeTaDePengyouMenDierqiJinghuaDianzishu'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="shuaizhang-he-ta-de-pengyou-men-dierqi-jinghua-dianzishu",
    version=ShuaizhangHeTaDePengyouMenDierqiJinghuaDianzishu.__version__,
    url="https://github.com/apachecn/shuaizhang-he-ta-de-pengyou-men-dierqi-jinghua-dianzishu",
    author=ShuaizhangHeTaDePengyouMenDierqiJinghuaDianzishu.__author__,
    author_email=ShuaizhangHeTaDePengyouMenDierqiJinghuaDianzishu.__email__,
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
    description="「帅张和他的朋友们」第二期精华电子书",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "shuaizhang-he-ta-de-pengyou-men-dierqi-jinghua-dianzishu=ShuaizhangHeTaDePengyouMenDierqiJinghuaDianzishu.__main__:main",
            "ShuaizhangHeTaDePengyouMenDierqiJinghuaDianzishu=ShuaizhangHeTaDePengyouMenDierqiJinghuaDianzishu.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
