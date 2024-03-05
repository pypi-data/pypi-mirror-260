#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import XinGainianMoniDianlu2FufankuiHeYunsuanFangdaqiJichu
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('XinGainianMoniDianlu2FufankuiHeYunsuanFangdaqiJichu'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="xin-gainian-moni-dianlu-2-fufankui-he-yunsuan-fangdaqi-jichu",
    version=XinGainianMoniDianlu2FufankuiHeYunsuanFangdaqiJichu.__version__,
    url="https://github.com/apachecn/xin-gainian-moni-dianlu-2-fufankui-he-yunsuan-fangdaqi-jichu",
    author=XinGainianMoniDianlu2FufankuiHeYunsuanFangdaqiJichu.__author__,
    author_email=XinGainianMoniDianlu2FufankuiHeYunsuanFangdaqiJichu.__email__,
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
    description="新概念模拟电路2-负反馈和运算放大器基础",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "xin-gainian-moni-dianlu-2-fufankui-he-yunsuan-fangdaqi-jichu=XinGainianMoniDianlu2FufankuiHeYunsuanFangdaqiJichu.__main__:main",
            "XinGainianMoniDianlu2FufankuiHeYunsuanFangdaqiJichu=XinGainianMoniDianlu2FufankuiHeYunsuanFangdaqiJichu.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
