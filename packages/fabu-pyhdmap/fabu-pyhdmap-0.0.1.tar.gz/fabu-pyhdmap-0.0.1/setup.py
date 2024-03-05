#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os 
from setuptools import setup, find_packages

MAJOR =0
MINOR =0
PATCH =1
VERSION = f"{MAJOR}.{MINOR}.{PATCH}"

def get_install_requires():
    reqs = [
            ]
    return reqs
setup(
	name = "fabu-pyhdmap",
	version = VERSION,
    author ="zhangqiuyang",
    author_email = "zhangqiuyang@fabu.ai",
    long_description_content_type="text/markdown",
	url = 'http://git.fabu.ai/zhangqiuyang/hdmapsdk-python',
	long_description = open('README.md',encoding="utf-8").read(),
    python_requires=">=3.7",
    install_requires=get_install_requires(),
	packages = find_packages(),
 	license = 'Apache',
    package_data={'': ['*.csv', '*.txt','.toml', "*.yaml", "*.conf"]},
    include_package_data=True
)