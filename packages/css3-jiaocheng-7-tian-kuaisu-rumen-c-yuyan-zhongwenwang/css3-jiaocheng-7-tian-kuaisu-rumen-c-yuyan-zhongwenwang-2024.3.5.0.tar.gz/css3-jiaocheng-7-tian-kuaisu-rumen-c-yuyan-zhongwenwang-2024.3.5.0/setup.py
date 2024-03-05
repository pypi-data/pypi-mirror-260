#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import Css3Jiaocheng7TianKuaisuRumenCYuyanZhongwenwang
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('Css3Jiaocheng7TianKuaisuRumenCYuyanZhongwenwang'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="css3-jiaocheng-7-tian-kuaisu-rumen-c-yuyan-zhongwenwang",
    version=Css3Jiaocheng7TianKuaisuRumenCYuyanZhongwenwang.__version__,
    url="https://github.com/apachecn/css3-jiaocheng-7-tian-kuaisu-rumen-c-yuyan-zhongwenwang",
    author=Css3Jiaocheng7TianKuaisuRumenCYuyanZhongwenwang.__author__,
    author_email=Css3Jiaocheng7TianKuaisuRumenCYuyanZhongwenwang.__email__,
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
    description="CSS3 教程，7 天快速入门（C 语言中文网）",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "css3-jiaocheng-7-tian-kuaisu-rumen-c-yuyan-zhongwenwang=Css3Jiaocheng7TianKuaisuRumenCYuyanZhongwenwang.__main__:main",
            "Css3Jiaocheng7TianKuaisuRumenCYuyanZhongwenwang=Css3Jiaocheng7TianKuaisuRumenCYuyanZhongwenwang.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
