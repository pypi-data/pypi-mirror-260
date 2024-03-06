#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import Opencv3HeQt5JisuanjiShijueChuyi
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('Opencv3HeQt5JisuanjiShijueChuyi'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="opencv3-he-qt5-jisuanji-shijue-chuyi",
    version=Opencv3HeQt5JisuanjiShijueChuyi.__version__,
    url="https://github.com/apachecn/opencv3-he-qt5-jisuanji-shijue-chuyi",
    author=Opencv3HeQt5JisuanjiShijueChuyi.__author__,
    author_email=Opencv3HeQt5JisuanjiShijueChuyi.__email__,
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
    description="OpenCV3 和 Qt5 计算机视觉（初译）",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "opencv3-he-qt5-jisuanji-shijue-chuyi=Opencv3HeQt5JisuanjiShijueChuyi.__main__:main",
            "Opencv3HeQt5JisuanjiShijueChuyi=Opencv3HeQt5JisuanjiShijueChuyi.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
