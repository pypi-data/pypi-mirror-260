#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import HitAlibabaBishiMianshiZhishiZhengli
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('HitAlibabaBishiMianshiZhishiZhengli'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="hit-alibaba-bishi-mianshi-zhishi-zhengli",
    version=HitAlibabaBishiMianshiZhishiZhengli.__version__,
    url="https://github.com/apachecn/hit-alibaba-bishi-mianshi-zhishi-zhengli",
    author=HitAlibabaBishiMianshiZhishiZhengli.__author__,
    author_email=HitAlibabaBishiMianshiZhishiZhengli.__email__,
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
    description="HIT-Alibaba 笔试面试知识整理",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "hit-alibaba-bishi-mianshi-zhishi-zhengli=HitAlibabaBishiMianshiZhishiZhengli.__main__:main",
            "HitAlibabaBishiMianshiZhishiZhengli=HitAlibabaBishiMianshiZhishiZhengli.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
