#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import BianxieGaozhiliangDaimaGaishanPythonChengxuDe91GeJianyi
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('BianxieGaozhiliangDaimaGaishanPythonChengxuDe91GeJianyi'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="bianxie-gaozhiliang-daima-gaishan-python-chengxu-de-91-ge-jianyi",
    version=BianxieGaozhiliangDaimaGaishanPythonChengxuDe91GeJianyi.__version__,
    url="https://github.com/apachecn/bianxie-gaozhiliang-daima-gaishan-python-chengxu-de-91-ge-jianyi",
    author=BianxieGaozhiliangDaimaGaishanPythonChengxuDe91GeJianyi.__author__,
    author_email=BianxieGaozhiliangDaimaGaishanPythonChengxuDe91GeJianyi.__email__,
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
    description="编写高质量代码改善 Python 程序的 91 个建议",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "bianxie-gaozhiliang-daima-gaishan-python-chengxu-de-91-ge-jianyi=BianxieGaozhiliangDaimaGaishanPythonChengxuDe91GeJianyi.__main__:main",
            "BianxieGaozhiliangDaimaGaishanPythonChengxuDe91GeJianyi=BianxieGaozhiliangDaimaGaishanPythonChengxuDe91GeJianyi.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
