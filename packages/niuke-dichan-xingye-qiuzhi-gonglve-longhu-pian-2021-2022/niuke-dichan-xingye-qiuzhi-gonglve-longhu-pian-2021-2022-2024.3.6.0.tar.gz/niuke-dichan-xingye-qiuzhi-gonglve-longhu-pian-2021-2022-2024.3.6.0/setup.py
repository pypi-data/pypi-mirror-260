#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import NiukeDichanXingyeQiuzhiGonglveLonghuPian20212022
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('NiukeDichanXingyeQiuzhiGonglveLonghuPian20212022'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="niuke-dichan-xingye-qiuzhi-gonglve-longhu-pian-2021-2022",
    version=NiukeDichanXingyeQiuzhiGonglveLonghuPian20212022.__version__,
    url="https://github.com/apachecn/niuke-dichan-xingye-qiuzhi-gonglve-longhu-pian-2021-2022",
    author=NiukeDichanXingyeQiuzhiGonglveLonghuPian20212022.__author__,
    author_email=NiukeDichanXingyeQiuzhiGonglveLonghuPian20212022.__email__,
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
    description="牛客地产行业求职攻略——龙湖篇 2021~2022",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "niuke-dichan-xingye-qiuzhi-gonglve-longhu-pian-2021-2022=NiukeDichanXingyeQiuzhiGonglveLonghuPian20212022.__main__:main",
            "NiukeDichanXingyeQiuzhiGonglveLonghuPian20212022=NiukeDichanXingyeQiuzhiGonglveLonghuPian20212022.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
