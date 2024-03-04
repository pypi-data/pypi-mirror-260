#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import Php55WebLingJichujiaochengKaifaYigeZaixianYueduWangzhan
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('Php55WebLingJichujiaochengKaifaYigeZaixianYueduWangzhan'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="php-5-5-web-ling-jichujiaocheng-kaifa-yige-zaixian-yuedu-wangzhan",
    version=Php55WebLingJichujiaochengKaifaYigeZaixianYueduWangzhan.__version__,
    url="https://github.com/apachecn/php-5-5-web-ling-jichujiaocheng-kaifa-yige-zaixian-yuedu-wangzhan",
    author=Php55WebLingJichujiaochengKaifaYigeZaixianYueduWangzhan.__author__,
    author_email=Php55WebLingJichujiaochengKaifaYigeZaixianYueduWangzhan.__email__,
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
    description="PHP 5.5 Web零基础教程：开发一个在线阅读网站",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "php-5-5-web-ling-jichujiaocheng-kaifa-yige-zaixian-yuedu-wangzhan=Php55WebLingJichujiaochengKaifaYigeZaixianYueduWangzhan.__main__:main",
            "Php55WebLingJichujiaochengKaifaYigeZaixianYueduWangzhan=Php55WebLingJichujiaochengKaifaYigeZaixianYueduWangzhan.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
