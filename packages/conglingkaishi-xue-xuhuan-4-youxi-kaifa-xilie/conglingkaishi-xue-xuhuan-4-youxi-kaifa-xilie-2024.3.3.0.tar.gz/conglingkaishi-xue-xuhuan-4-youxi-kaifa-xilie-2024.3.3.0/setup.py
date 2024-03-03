#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import ConglingkaishiXueXuhuan4YouxiKaifaXilie
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('ConglingkaishiXueXuhuan4YouxiKaifaXilie'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="conglingkaishi-xue-xuhuan-4-youxi-kaifa-xilie",
    version=ConglingkaishiXueXuhuan4YouxiKaifaXilie.__version__,
    url="https://github.com/apachecn/conglingkaishi-xue-xuhuan-4-youxi-kaifa-xilie",
    author=ConglingkaishiXueXuhuan4YouxiKaifaXilie.__author__,
    author_email=ConglingkaishiXueXuhuan4YouxiKaifaXilie.__email__,
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
    description="从零开始学虚幻4游戏开发系列",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "conglingkaishi-xue-xuhuan-4-youxi-kaifa-xilie=ConglingkaishiXueXuhuan4YouxiKaifaXilie.__main__:main",
            "ConglingkaishiXueXuhuan4YouxiKaifaXilie=ConglingkaishiXueXuhuan4YouxiKaifaXilie.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
