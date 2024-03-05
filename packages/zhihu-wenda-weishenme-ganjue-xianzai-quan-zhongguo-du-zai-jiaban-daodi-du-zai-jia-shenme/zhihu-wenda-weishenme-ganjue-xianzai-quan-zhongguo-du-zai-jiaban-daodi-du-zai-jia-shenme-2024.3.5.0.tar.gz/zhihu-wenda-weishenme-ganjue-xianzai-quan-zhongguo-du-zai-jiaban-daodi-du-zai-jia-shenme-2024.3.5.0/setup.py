#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import ZhihuWendaWeishenmeGanjueXianzaiQuanZhongguoDuZaiJiabanDaodiDuZaiJiaShenme
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('ZhihuWendaWeishenmeGanjueXianzaiQuanZhongguoDuZaiJiabanDaodiDuZaiJiaShenme'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="zhihu-wenda-weishenme-ganjue-xianzai-quan-zhongguo-du-zai-jiaban-daodi-du-zai-jia-shenme",
    version=ZhihuWendaWeishenmeGanjueXianzaiQuanZhongguoDuZaiJiabanDaodiDuZaiJiaShenme.__version__,
    url="https://github.com/apachecn/zhihu-wenda-weishenme-ganjue-xianzai-quan-zhongguo-du-zai-jiaban-daodi-du-zai-jia-shenme",
    author=ZhihuWendaWeishenmeGanjueXianzaiQuanZhongguoDuZaiJiabanDaodiDuZaiJiaShenme.__author__,
    author_email=ZhihuWendaWeishenmeGanjueXianzaiQuanZhongguoDuZaiJiabanDaodiDuZaiJiaShenme.__email__,
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
    description="知乎问答：为什么感觉现在全中国都在加班，到底都在加什么？",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "zhihu-wenda-weishenme-ganjue-xianzai-quan-zhongguo-du-zai-jiaban-daodi-du-zai-jia-shenme=ZhihuWendaWeishenmeGanjueXianzaiQuanZhongguoDuZaiJiabanDaodiDuZaiJiaShenme.__main__:main",
            "ZhihuWendaWeishenmeGanjueXianzaiQuanZhongguoDuZaiJiabanDaodiDuZaiJiaShenme=ZhihuWendaWeishenmeGanjueXianzaiQuanZhongguoDuZaiJiabanDaodiDuZaiJiaShenme.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
