#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import RealTimeRendering3rdTilianZongjie
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('RealTimeRendering3rdTilianZongjie'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="real-time-rendering-3rd-tilian-zongjie",
    version=RealTimeRendering3rdTilianZongjie.__version__,
    url="https://github.com/apachecn/real-time-rendering-3rd-tilian-zongjie",
    author=RealTimeRendering3rdTilianZongjie.__author__,
    author_email=RealTimeRendering3rdTilianZongjie.__email__,
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
    description="《Real-Time Rendering 3rd》 提炼总结",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "real-time-rendering-3rd-tilian-zongjie=RealTimeRendering3rdTilianZongjie.__main__:main",
            "RealTimeRendering3rdTilianZongjie=RealTimeRendering3rdTilianZongjie.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
