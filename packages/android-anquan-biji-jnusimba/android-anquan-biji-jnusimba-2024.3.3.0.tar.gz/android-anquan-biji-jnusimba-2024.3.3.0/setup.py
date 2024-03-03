#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import AndroidAnquanBijiJnusimba
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('AndroidAnquanBijiJnusimba'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="android-anquan-biji-jnusimba",
    version=AndroidAnquanBijiJnusimba.__version__,
    url="https://github.com/apachecn/android-anquan-biji-jnusimba",
    author=AndroidAnquanBijiJnusimba.__author__,
    author_email=AndroidAnquanBijiJnusimba.__email__,
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
    description="Android 安全笔记（JnuSimba）",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "android-anquan-biji-jnusimba=AndroidAnquanBijiJnusimba.__main__:main",
            "AndroidAnquanBijiJnusimba=AndroidAnquanBijiJnusimba.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
