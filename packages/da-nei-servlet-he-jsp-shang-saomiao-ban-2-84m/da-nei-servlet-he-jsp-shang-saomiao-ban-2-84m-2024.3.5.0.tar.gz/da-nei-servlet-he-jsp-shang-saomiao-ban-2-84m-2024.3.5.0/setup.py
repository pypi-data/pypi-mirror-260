#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import DaNeiServletHeJspShangSaomiaoBan284m
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('DaNeiServletHeJspShangSaomiaoBan284m'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="da-nei-servlet-he-jsp-shang-saomiao-ban-2-84m",
    version=DaNeiServletHeJspShangSaomiaoBan284m.__version__,
    url="https://github.com/apachecn/da-nei-servlet-he-jsp-shang-saomiao-ban-2-84m",
    author=DaNeiServletHeJspShangSaomiaoBan284m.__author__,
    author_email=DaNeiServletHeJspShangSaomiaoBan284m.__email__,
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
    description="达内 Servlet 和 JSP（上）_扫描版_2.84M",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "da-nei-servlet-he-jsp-shang-saomiao-ban-2-84m=DaNeiServletHeJspShangSaomiaoBan284m.__main__:main",
            "DaNeiServletHeJspShangSaomiaoBan284m=DaNeiServletHeJspShangSaomiaoBan284m.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
