#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import SklearnYuTensorflowJiqiXuexiShiyongZhinanZhongwenban2018620
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('SklearnYuTensorflowJiqiXuexiShiyongZhinanZhongwenban2018620'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="sklearn-yu-tensorflow-jiqi-xuexi-shiyong-zhinan-zhongwenban-2018-6-20",
    version=SklearnYuTensorflowJiqiXuexiShiyongZhinanZhongwenban2018620.__version__,
    url="https://github.com/apachecn/sklearn-yu-tensorflow-jiqi-xuexi-shiyong-zhinan-zhongwenban-2018-6-20",
    author=SklearnYuTensorflowJiqiXuexiShiyongZhinanZhongwenban2018620.__author__,
    author_email=SklearnYuTensorflowJiqiXuexiShiyongZhinanZhongwenban2018620.__email__,
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
    description="Sklearn 与 TensorFlow 机器学习实用指南中文版 2018.6.20",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "sklearn-yu-tensorflow-jiqi-xuexi-shiyong-zhinan-zhongwenban-2018-6-20=SklearnYuTensorflowJiqiXuexiShiyongZhinanZhongwenban2018620.__main__:main",
            "SklearnYuTensorflowJiqiXuexiShiyongZhinanZhongwenban2018620=SklearnYuTensorflowJiqiXuexiShiyongZhinanZhongwenban2018620.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
