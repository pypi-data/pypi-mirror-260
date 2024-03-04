#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import JiqiXuexiXunlianMijiMachineLearningYearningZhongwenban
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('JiqiXuexiXunlianMijiMachineLearningYearningZhongwenban'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="jiqi-xuexi-xunlian-miji-machine-learning-yearning-zhongwenban",
    version=JiqiXuexiXunlianMijiMachineLearningYearningZhongwenban.__version__,
    url="https://github.com/apachecn/jiqi-xuexi-xunlian-miji-machine-learning-yearning-zhongwenban",
    author=JiqiXuexiXunlianMijiMachineLearningYearningZhongwenban.__author__,
    author_email=JiqiXuexiXunlianMijiMachineLearningYearningZhongwenban.__email__,
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
    description="机器学习训练秘籍（Machine Learning Yearning 中文版）",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "jiqi-xuexi-xunlian-miji-machine-learning-yearning-zhongwenban=JiqiXuexiXunlianMijiMachineLearningYearningZhongwenban.__main__:main",
            "JiqiXuexiXunlianMijiMachineLearningYearningZhongwenban=JiqiXuexiXunlianMijiMachineLearningYearningZhongwenban.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
