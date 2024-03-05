#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import ZhongwenVocaloidChuangzuoRumenjiaochengV110Dg
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('ZhongwenVocaloidChuangzuoRumenjiaochengV110Dg'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="zhongwen-vocaloid-chuangzuo-rumenjiaocheng-v1-1-0-dg",
    version=ZhongwenVocaloidChuangzuoRumenjiaochengV110Dg.__version__,
    url="https://github.com/apachecn/zhongwen-vocaloid-chuangzuo-rumenjiaocheng-v1-1-0-dg",
    author=ZhongwenVocaloidChuangzuoRumenjiaochengV110Dg.__author__,
    author_email=ZhongwenVocaloidChuangzuoRumenjiaochengV110Dg.__email__,
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
    description="中文 Vocaloid 创作入门教程 v1.1.0.DG",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "zhongwen-vocaloid-chuangzuo-rumenjiaocheng-v1-1-0-dg=ZhongwenVocaloidChuangzuoRumenjiaochengV110Dg.__main__:main",
            "ZhongwenVocaloidChuangzuoRumenjiaochengV110Dg=ZhongwenVocaloidChuangzuoRumenjiaochengV110Dg.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
