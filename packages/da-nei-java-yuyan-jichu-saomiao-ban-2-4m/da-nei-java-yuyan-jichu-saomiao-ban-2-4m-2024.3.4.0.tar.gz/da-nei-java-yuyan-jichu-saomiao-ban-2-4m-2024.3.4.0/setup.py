#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import DaNeiJavaYuyanJichuSaomiaoBan24m
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('DaNeiJavaYuyanJichuSaomiaoBan24m'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="da-nei-java-yuyan-jichu-saomiao-ban-2-4m",
    version=DaNeiJavaYuyanJichuSaomiaoBan24m.__version__,
    url="https://github.com/apachecn/da-nei-java-yuyan-jichu-saomiao-ban-2-4m",
    author=DaNeiJavaYuyanJichuSaomiaoBan24m.__author__,
    author_email=DaNeiJavaYuyanJichuSaomiaoBan24m.__email__,
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
    description="达内 Java 语言基础_扫描版_2.4M",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "da-nei-java-yuyan-jichu-saomiao-ban-2-4m=DaNeiJavaYuyanJichuSaomiaoBan24m.__main__:main",
            "DaNeiJavaYuyanJichuSaomiaoBan24m=DaNeiJavaYuyanJichuSaomiaoBan24m.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
