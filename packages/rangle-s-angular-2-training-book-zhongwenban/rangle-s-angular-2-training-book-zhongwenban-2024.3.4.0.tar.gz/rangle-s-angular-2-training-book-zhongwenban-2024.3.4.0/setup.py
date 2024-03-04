#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import RangleSAngular2TrainingBookZhongwenban
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('RangleSAngular2TrainingBookZhongwenban'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="rangle-s-angular-2-training-book-zhongwenban",
    version=RangleSAngular2TrainingBookZhongwenban.__version__,
    url="https://github.com/apachecn/rangle-s-angular-2-training-book-zhongwenban",
    author=RangleSAngular2TrainingBookZhongwenban.__author__,
    author_email=RangleSAngular2TrainingBookZhongwenban.__email__,
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
    description="Rangle's Angular 2 Training Book 中文版",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "rangle-s-angular-2-training-book-zhongwenban=RangleSAngular2TrainingBookZhongwenban.__main__:main",
            "RangleSAngular2TrainingBookZhongwenban=RangleSAngular2TrainingBookZhongwenban.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
