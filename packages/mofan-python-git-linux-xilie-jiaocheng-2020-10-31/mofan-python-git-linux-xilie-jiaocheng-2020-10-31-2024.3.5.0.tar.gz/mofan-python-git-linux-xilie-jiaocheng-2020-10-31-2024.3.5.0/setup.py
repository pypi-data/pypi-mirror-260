#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import MofanPythonGitLinuxXilieJiaocheng20201031
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('MofanPythonGitLinuxXilieJiaocheng20201031'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="mofan-python-git-linux-xilie-jiaocheng-2020-10-31",
    version=MofanPythonGitLinuxXilieJiaocheng20201031.__version__,
    url="https://github.com/apachecn/mofan-python-git-linux-xilie-jiaocheng-2020-10-31",
    author=MofanPythonGitLinuxXilieJiaocheng20201031.__author__,
    author_email=MofanPythonGitLinuxXilieJiaocheng20201031.__email__,
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
    description="莫烦 Python、Git、Linux 系列教程 2020.10.31",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "mofan-python-git-linux-xilie-jiaocheng-2020-10-31=MofanPythonGitLinuxXilieJiaocheng20201031.__main__:main",
            "MofanPythonGitLinuxXilieJiaocheng20201031=MofanPythonGitLinuxXilieJiaocheng20201031.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
