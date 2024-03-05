#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import XinGainianMoniDianlu3YunsuanFangdaqiDePinlvtexingHeLvboqi
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('XinGainianMoniDianlu3YunsuanFangdaqiDePinlvtexingHeLvboqi'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="xin-gainian-moni-dianlu-3-yunsuan-fangdaqi-de-pinlvtexing-he-lvboqi",
    version=XinGainianMoniDianlu3YunsuanFangdaqiDePinlvtexingHeLvboqi.__version__,
    url="https://github.com/apachecn/xin-gainian-moni-dianlu-3-yunsuan-fangdaqi-de-pinlvtexing-he-lvboqi",
    author=XinGainianMoniDianlu3YunsuanFangdaqiDePinlvtexingHeLvboqi.__author__,
    author_email=XinGainianMoniDianlu3YunsuanFangdaqiDePinlvtexingHeLvboqi.__email__,
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
    description="新概念模拟电路3-运算放大器的频率特性和滤波器",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "xin-gainian-moni-dianlu-3-yunsuan-fangdaqi-de-pinlvtexing-he-lvboqi=XinGainianMoniDianlu3YunsuanFangdaqiDePinlvtexingHeLvboqi.__main__:main",
            "XinGainianMoniDianlu3YunsuanFangdaqiDePinlvtexingHeLvboqi=XinGainianMoniDianlu3YunsuanFangdaqiDePinlvtexingHeLvboqi.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
