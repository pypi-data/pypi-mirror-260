#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import LearningSparkZhongwenban38Zhang
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('LearningSparkZhongwenban38Zhang'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="learning-spark-zhongwenban-3-8-zhang",
    version=LearningSparkZhongwenban38Zhang.__version__,
    url="https://github.com/apachecn/learning-spark-zhongwenban-3-8-zhang",
    author=LearningSparkZhongwenban38Zhang.__author__,
    author_email=LearningSparkZhongwenban38Zhang.__email__,
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
    description="Learning Spark 中文版 3-8 章",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "learning-spark-zhongwenban-3-8-zhang=LearningSparkZhongwenban38Zhang.__main__:main",
            "LearningSparkZhongwenban38Zhang=LearningSparkZhongwenban38Zhang.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
