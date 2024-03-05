#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：tea -> setup
@IDE    ：PyCharm
@Author ：Mr. T
@Date   ：2024/2/22 17:27
@Desc   ：kity_stu
=================================================="""
from setuptools import setup, find_packages

setup(
  name="teatest",
  version="0.1.2",
  packages=find_packages(),
  project_urls={
    'Source': 'https://github.com/Easonwt/teatest',
  },
  include_package_data=True,
  install_requires=[
    # 在这里列出你的库所需的其他Python包
    "twine",
    "idna",
    "pip"
  ],

  author="Easonwt",
  author_email="wangkeqiaosheng@gmail.com",
  description="This is a tea test file",
  # long_description=open("README.md").read(),
  long_description_content_type="text/markdown",
  license="MIT",
  url="https://github.com/Easonwt/teatest",
  classifiers=[
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
  ],
)
