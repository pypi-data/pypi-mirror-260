#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import JiyuEosNodeJsDeDappGongchengxiangmuShizhanQuZhongxinhuaJiaoyisuo
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('JiyuEosNodeJsDeDappGongchengxiangmuShizhanQuZhongxinhuaJiaoyisuo'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="jiyu-eos-node-js-de-dapp-gongchengxiangmu-shizhan-qu-zhongxinhua-jiaoyisuo",
    version=JiyuEosNodeJsDeDappGongchengxiangmuShizhanQuZhongxinhuaJiaoyisuo.__version__,
    url="https://github.com/apachecn/jiyu-eos-node-js-de-dapp-gongchengxiangmu-shizhan-qu-zhongxinhua-jiaoyisuo",
    author=JiyuEosNodeJsDeDappGongchengxiangmuShizhanQuZhongxinhuaJiaoyisuo.__author__,
    author_email=JiyuEosNodeJsDeDappGongchengxiangmuShizhanQuZhongxinhuaJiaoyisuo.__email__,
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
    description="基于EOS-Node.js的DApp工程项目实战---去中心化交易所",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "jiyu-eos-node-js-de-dapp-gongchengxiangmu-shizhan-qu-zhongxinhua-jiaoyisuo=JiyuEosNodeJsDeDappGongchengxiangmuShizhanQuZhongxinhuaJiaoyisuo.__main__:main",
            "JiyuEosNodeJsDeDappGongchengxiangmuShizhanQuZhongxinhuaJiaoyisuo=JiyuEosNodeJsDeDappGongchengxiangmuShizhanQuZhongxinhuaJiaoyisuo.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
