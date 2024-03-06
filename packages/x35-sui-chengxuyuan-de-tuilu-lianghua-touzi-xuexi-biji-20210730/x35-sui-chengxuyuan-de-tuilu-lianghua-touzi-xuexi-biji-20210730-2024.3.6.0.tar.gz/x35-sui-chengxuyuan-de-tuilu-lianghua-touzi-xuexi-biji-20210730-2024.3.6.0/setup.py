#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import X35SuiChengxuyuanDeTuiluLianghuaTouziXuexiBiji20210730
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('X35SuiChengxuyuanDeTuiluLianghuaTouziXuexiBiji20210730'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="x35-sui-chengxuyuan-de-tuilu-lianghua-touzi-xuexi-biji-20210730",
    version=X35SuiChengxuyuanDeTuiluLianghuaTouziXuexiBiji20210730.__version__,
    url="https://github.com/apachecn/x35-sui-chengxuyuan-de-tuilu-lianghua-touzi-xuexi-biji-20210730",
    author=X35SuiChengxuyuanDeTuiluLianghuaTouziXuexiBiji20210730.__author__,
    author_email=X35SuiChengxuyuanDeTuiluLianghuaTouziXuexiBiji20210730.__email__,
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
    description="35岁程序员的退路：量化投资学习笔记 20210730",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "x35-sui-chengxuyuan-de-tuilu-lianghua-touzi-xuexi-biji-20210730=X35SuiChengxuyuanDeTuiluLianghuaTouziXuexiBiji20210730.__main__:main",
            "X35SuiChengxuyuanDeTuiluLianghuaTouziXuexiBiji20210730=X35SuiChengxuyuanDeTuiluLianghuaTouziXuexiBiji20210730.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
