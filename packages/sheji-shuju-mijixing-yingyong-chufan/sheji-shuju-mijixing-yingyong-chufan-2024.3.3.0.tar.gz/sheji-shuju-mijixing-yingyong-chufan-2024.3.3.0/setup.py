#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import ShejiShujuMijixingYingyongChufan
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('ShejiShujuMijixingYingyongChufan'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="sheji-shuju-mijixing-yingyong-chufan",
    version=ShejiShujuMijixingYingyongChufan.__version__,
    url="https://github.com/apachecn/sheji-shuju-mijixing-yingyong-chufan",
    author=ShejiShujuMijixingYingyongChufan.__author__,
    author_email=ShejiShujuMijixingYingyongChufan.__email__,
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
    description="设计数据密集型应用（初翻）",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "sheji-shuju-mijixing-yingyong-chufan=ShejiShujuMijixingYingyongChufan.__main__:main",
            "ShejiShujuMijixingYingyongChufan=ShejiShujuMijixingYingyongChufan.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
