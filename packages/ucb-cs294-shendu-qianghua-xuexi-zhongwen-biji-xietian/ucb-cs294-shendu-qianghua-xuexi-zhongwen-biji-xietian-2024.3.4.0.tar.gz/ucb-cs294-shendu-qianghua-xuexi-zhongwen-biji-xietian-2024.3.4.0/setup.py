#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import UcbCs294ShenduQianghuaXuexiZhongwenBijiXietian
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('UcbCs294ShenduQianghuaXuexiZhongwenBijiXietian'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="ucb-cs294-shendu-qianghua-xuexi-zhongwen-biji-xietian",
    version=UcbCs294ShenduQianghuaXuexiZhongwenBijiXietian.__version__,
    url="https://github.com/apachecn/ucb-cs294-shendu-qianghua-xuexi-zhongwen-biji-xietian",
    author=UcbCs294ShenduQianghuaXuexiZhongwenBijiXietian.__author__,
    author_email=UcbCs294ShenduQianghuaXuexiZhongwenBijiXietian.__email__,
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
    description="UCB CS294 深度强化学习中文笔记（谢天）",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "ucb-cs294-shendu-qianghua-xuexi-zhongwen-biji-xietian=UcbCs294ShenduQianghuaXuexiZhongwenBijiXietian.__main__:main",
            "UcbCs294ShenduQianghuaXuexiZhongwenBijiXietian=UcbCs294ShenduQianghuaXuexiZhongwenBijiXietian.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
