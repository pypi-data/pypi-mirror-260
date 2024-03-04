#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import Bootstrap2YonghuZhinanWaiBowang
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('Bootstrap2YonghuZhinanWaiBowang'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="bootstrap2-yonghu-zhinan-wai-bowang",
    version=Bootstrap2YonghuZhinanWaiBowang.__version__,
    url="https://github.com/apachecn/bootstrap2-yonghu-zhinan-wai-bowang",
    author=Bootstrap2YonghuZhinanWaiBowang.__author__,
    author_email=Bootstrap2YonghuZhinanWaiBowang.__email__,
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
    description="Bootstrap2 用户指南（歪脖网）",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "bootstrap2-yonghu-zhinan-wai-bowang=Bootstrap2YonghuZhinanWaiBowang.__main__:main",
            "Bootstrap2YonghuZhinanWaiBowang=Bootstrap2YonghuZhinanWaiBowang.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
