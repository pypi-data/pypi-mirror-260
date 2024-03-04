#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import TensorflowZhongwenWendang18Juejin2018519
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('TensorflowZhongwenWendang18Juejin2018519'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="tensorflow-zhongwen-wendang-1-8-juejin-2018-5-19",
    version=TensorflowZhongwenWendang18Juejin2018519.__version__,
    url="https://github.com/apachecn/tensorflow-zhongwen-wendang-1-8-juejin-2018-5-19",
    author=TensorflowZhongwenWendang18Juejin2018519.__author__,
    author_email=TensorflowZhongwenWendang18Juejin2018519.__email__,
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
    description="TensorFlow 中文文档 1.8 掘金 2018.5.19",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "tensorflow-zhongwen-wendang-1-8-juejin-2018-5-19=TensorflowZhongwenWendang18Juejin2018519.__main__:main",
            "TensorflowZhongwenWendang18Juejin2018519=TensorflowZhongwenWendang18Juejin2018519.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
