#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import KiraXiandaixiaoJuhuaWan2017Quan
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('KiraXiandaixiaoJuhuaWan2017Quan'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="kira-xiandaixiao-juhua-wan-2017-quan",
    version=KiraXiandaixiaoJuhuaWan2017Quan.__version__,
    url="https://github.com/apachecn/kira-xiandaixiao-juhua-wan-2017-quan",
    author=KiraXiandaixiaoJuhuaWan2017Quan.__author__,
    author_email=KiraXiandaixiaoJuhuaWan2017Quan.__email__,
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
    description="Kira 线代小菊花丸 2017（全）",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "kira-xiandaixiao-juhua-wan-2017-quan=KiraXiandaixiaoJuhuaWan2017Quan.__main__:main",
            "KiraXiandaixiaoJuhuaWan2017Quan=KiraXiandaixiaoJuhuaWan2017Quan.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
