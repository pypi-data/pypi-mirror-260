#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import GugeJisuanSiweiKechengZhongwenban
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('GugeJisuanSiweiKechengZhongwenban'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="guge-jisuan-siwei-kecheng-zhongwenban",
    version=GugeJisuanSiweiKechengZhongwenban.__version__,
    url="https://github.com/apachecn/guge-jisuan-siwei-kecheng-zhongwenban",
    author=GugeJisuanSiweiKechengZhongwenban.__author__,
    author_email=GugeJisuanSiweiKechengZhongwenban.__email__,
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
    description="谷歌计算思维课程（中文版）",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "guge-jisuan-siwei-kecheng-zhongwenban=GugeJisuanSiweiKechengZhongwenban.__main__:main",
            "GugeJisuanSiweiKechengZhongwenban=GugeJisuanSiweiKechengZhongwenban.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
