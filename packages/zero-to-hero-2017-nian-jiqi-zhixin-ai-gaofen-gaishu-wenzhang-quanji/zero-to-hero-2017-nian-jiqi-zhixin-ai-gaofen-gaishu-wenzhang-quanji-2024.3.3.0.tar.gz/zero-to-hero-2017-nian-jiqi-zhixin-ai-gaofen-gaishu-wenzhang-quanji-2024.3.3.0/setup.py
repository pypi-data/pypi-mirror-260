#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import ZeroToHero2017NianJiqiZhixinAiGaofenGaishuWenzhangQuanji
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('ZeroToHero2017NianJiqiZhixinAiGaofenGaishuWenzhangQuanji'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="zero-to-hero-2017-nian-jiqi-zhixin-ai-gaofen-gaishu-wenzhang-quanji",
    version=ZeroToHero2017NianJiqiZhixinAiGaofenGaishuWenzhangQuanji.__version__,
    url="https://github.com/apachecn/zero-to-hero-2017-nian-jiqi-zhixin-ai-gaofen-gaishu-wenzhang-quanji",
    author=ZeroToHero2017NianJiqiZhixinAiGaofenGaishuWenzhangQuanji.__author__,
    author_email=ZeroToHero2017NianJiqiZhixinAiGaofenGaishuWenzhangQuanji.__email__,
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
    description="Zero to Hero：2017年机器之心AI高分概述文章全集",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "zero-to-hero-2017-nian-jiqi-zhixin-ai-gaofen-gaishu-wenzhang-quanji=ZeroToHero2017NianJiqiZhixinAiGaofenGaishuWenzhangQuanji.__main__:main",
            "ZeroToHero2017NianJiqiZhixinAiGaofenGaishuWenzhangQuanji=ZeroToHero2017NianJiqiZhixinAiGaofenGaishuWenzhangQuanji.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
