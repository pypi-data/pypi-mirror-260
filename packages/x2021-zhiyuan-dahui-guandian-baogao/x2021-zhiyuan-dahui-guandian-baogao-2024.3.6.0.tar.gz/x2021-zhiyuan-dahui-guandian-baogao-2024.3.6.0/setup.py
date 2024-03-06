#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import X2021ZhiyuanDahuiGuandianBaogao
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('X2021ZhiyuanDahuiGuandianBaogao'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="x2021-zhiyuan-dahui-guandian-baogao",
    version=X2021ZhiyuanDahuiGuandianBaogao.__version__,
    url="https://github.com/apachecn/x2021-zhiyuan-dahui-guandian-baogao",
    author=X2021ZhiyuanDahuiGuandianBaogao.__author__,
    author_email=X2021ZhiyuanDahuiGuandianBaogao.__email__,
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
    description="2021智源大会观点报告",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "x2021-zhiyuan-dahui-guandian-baogao=X2021ZhiyuanDahuiGuandianBaogao.__main__:main",
            "X2021ZhiyuanDahuiGuandianBaogao=X2021ZhiyuanDahuiGuandianBaogao.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
