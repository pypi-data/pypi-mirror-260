#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import BatJiqiXuexiMianshi1000TiXilieDi1325Ti
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('BatJiqiXuexiMianshi1000TiXilieDi1325Ti'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="bat-jiqi-xuexi-mianshi-1000-ti-xilie-di-1-325-ti",
    version=BatJiqiXuexiMianshi1000TiXilieDi1325Ti.__version__,
    url="https://github.com/apachecn/bat-jiqi-xuexi-mianshi-1000-ti-xilie-di-1-325-ti",
    author=BatJiqiXuexiMianshi1000TiXilieDi1325Ti.__author__,
    author_email=BatJiqiXuexiMianshi1000TiXilieDi1325Ti.__email__,
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
    description="BAT 机器学习面试 1000 题系列（第 1~325 题）",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "bat-jiqi-xuexi-mianshi-1000-ti-xilie-di-1-325-ti=BatJiqiXuexiMianshi1000TiXilieDi1325Ti.__main__:main",
            "BatJiqiXuexiMianshi1000TiXilieDi1325Ti=BatJiqiXuexiMianshi1000TiXilieDi1325Ti.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
