#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import SpringBoot211ReleaseZhongwenWendang
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('SpringBoot211ReleaseZhongwenWendang'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="spring-boot-2-1-1-release-zhongwen-wendang",
    version=SpringBoot211ReleaseZhongwenWendang.__version__,
    url="https://github.com/apachecn/spring-boot-2-1-1-release-zhongwen-wendang",
    author=SpringBoot211ReleaseZhongwenWendang.__author__,
    author_email=SpringBoot211ReleaseZhongwenWendang.__email__,
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
    description="Spring Boot 2.1.1.RELEASE 中文文档",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "spring-boot-2-1-1-release-zhongwen-wendang=SpringBoot211ReleaseZhongwenWendang.__main__:main",
            "SpringBoot211ReleaseZhongwenWendang=SpringBoot211ReleaseZhongwenWendang.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
