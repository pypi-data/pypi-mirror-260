#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import WeiYewuliangShenDazaoAliWenyuYonghuJiNeirongYunyingPingtaiJishuShijian
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('WeiYewuliangShenDazaoAliWenyuYonghuJiNeirongYunyingPingtaiJishuShijian'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="wei-yewuliang-shen-dazao-ali-wenyu-yonghu-ji-neirong-yunying-pingtai-jishu-shijian",
    version=WeiYewuliangShenDazaoAliWenyuYonghuJiNeirongYunyingPingtaiJishuShijian.__version__,
    url="https://github.com/apachecn/wei-yewuliang-shen-dazao-ali-wenyu-yonghu-ji-neirong-yunying-pingtai-jishu-shijian",
    author=WeiYewuliangShenDazaoAliWenyuYonghuJiNeirongYunyingPingtaiJishuShijian.__author__,
    author_email=WeiYewuliangShenDazaoAliWenyuYonghuJiNeirongYunyingPingtaiJishuShijian.__email__,
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
    description="为业务量身打造——阿里文娱用户及内容运营平台技术实践",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "wei-yewuliang-shen-dazao-ali-wenyu-yonghu-ji-neirong-yunying-pingtai-jishu-shijian=WeiYewuliangShenDazaoAliWenyuYonghuJiNeirongYunyingPingtaiJishuShijian.__main__:main",
            "WeiYewuliangShenDazaoAliWenyuYonghuJiNeirongYunyingPingtaiJishuShijian=WeiYewuliangShenDazaoAliWenyuYonghuJiNeirongYunyingPingtaiJishuShijian.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
