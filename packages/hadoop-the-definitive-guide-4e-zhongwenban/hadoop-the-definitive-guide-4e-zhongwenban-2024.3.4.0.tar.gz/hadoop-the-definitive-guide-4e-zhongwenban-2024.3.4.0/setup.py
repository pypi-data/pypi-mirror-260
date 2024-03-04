#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import HadoopTheDefinitiveGuide4eZhongwenban
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('HadoopTheDefinitiveGuide4eZhongwenban'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="hadoop-the-definitive-guide-4e-zhongwenban",
    version=HadoopTheDefinitiveGuide4eZhongwenban.__version__,
    url="https://github.com/apachecn/hadoop-the-definitive-guide-4e-zhongwenban",
    author=HadoopTheDefinitiveGuide4eZhongwenban.__author__,
    author_email=HadoopTheDefinitiveGuide4eZhongwenban.__email__,
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
    description="Hadoop The Definitive Guide 4e 中文版",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "hadoop-the-definitive-guide-4e-zhongwenban=HadoopTheDefinitiveGuide4eZhongwenban.__main__:main",
            "HadoopTheDefinitiveGuide4eZhongwenban=HadoopTheDefinitiveGuide4eZhongwenban.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
