#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import Pyqt5ZhongwenJiaocheng
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('Pyqt5ZhongwenJiaocheng'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="pyqt5-zhongwen-jiaocheng",
    version=Pyqt5ZhongwenJiaocheng.__version__,
    url="https://github.com/apachecn/pyqt5-zhongwen-jiaocheng",
    author=Pyqt5ZhongwenJiaocheng.__author__,
    author_email=Pyqt5ZhongwenJiaocheng.__email__,
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
    description="PyQt5 中文教程",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "pyqt5-zhongwen-jiaocheng=Pyqt5ZhongwenJiaocheng.__main__:main",
            "Pyqt5ZhongwenJiaocheng=Pyqt5ZhongwenJiaocheng.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
