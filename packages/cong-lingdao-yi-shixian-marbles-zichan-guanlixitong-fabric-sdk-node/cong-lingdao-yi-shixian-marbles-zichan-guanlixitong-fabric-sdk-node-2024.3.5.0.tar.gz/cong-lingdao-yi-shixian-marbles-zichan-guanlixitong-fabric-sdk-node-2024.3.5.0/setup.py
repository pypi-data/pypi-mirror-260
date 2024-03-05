#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import CongLingdaoYiShixianMarblesZichanGuanlixitongFabricSdkNode
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('CongLingdaoYiShixianMarblesZichanGuanlixitongFabricSdkNode'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="cong-lingdao-yi-shixian-marbles-zichan-guanlixitong-fabric-sdk-node",
    version=CongLingdaoYiShixianMarblesZichanGuanlixitongFabricSdkNode.__version__,
    url="https://github.com/apachecn/cong-lingdao-yi-shixian-marbles-zichan-guanlixitong-fabric-sdk-node",
    author=CongLingdaoYiShixianMarblesZichanGuanlixitongFabricSdkNode.__author__,
    author_email=CongLingdaoYiShixianMarblesZichanGuanlixitongFabricSdkNode.__email__,
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
    description="从零到壹实现Marbles资产管理系统 （Fabric-SDK-Node）",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "cong-lingdao-yi-shixian-marbles-zichan-guanlixitong-fabric-sdk-node=CongLingdaoYiShixianMarblesZichanGuanlixitongFabricSdkNode.__main__:main",
            "CongLingdaoYiShixianMarblesZichanGuanlixitongFabricSdkNode=CongLingdaoYiShixianMarblesZichanGuanlixitongFabricSdkNode.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
