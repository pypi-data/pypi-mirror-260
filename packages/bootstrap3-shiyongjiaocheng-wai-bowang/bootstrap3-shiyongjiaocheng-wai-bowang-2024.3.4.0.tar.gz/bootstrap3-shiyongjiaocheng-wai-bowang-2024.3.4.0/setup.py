#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import Bootstrap3ShiyongjiaochengWaiBowang
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('Bootstrap3ShiyongjiaochengWaiBowang'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="bootstrap3-shiyongjiaocheng-wai-bowang",
    version=Bootstrap3ShiyongjiaochengWaiBowang.__version__,
    url="https://github.com/apachecn/bootstrap3-shiyongjiaocheng-wai-bowang",
    author=Bootstrap3ShiyongjiaochengWaiBowang.__author__,
    author_email=Bootstrap3ShiyongjiaochengWaiBowang.__email__,
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
    description="Bootstrap3 实用教程（歪脖网）",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "bootstrap3-shiyongjiaocheng-wai-bowang=Bootstrap3ShiyongjiaochengWaiBowang.__main__:main",
            "Bootstrap3ShiyongjiaochengWaiBowang=Bootstrap3ShiyongjiaochengWaiBowang.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
