#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os 
from setuptools import setup, find_packages

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

def get_version():
    scope = {}
    version = '1.1'
    version_file = os.path.join(THIS_DIR, "dbpystream", "version.py")
    if os.path.exists(version_file):
        with open(version_file) as fp:
            exec(fp.read(), scope)
        version = scope.get('__version__', '1.1')
    return version

def get_install_requires():
    reqs = [
            'pandas>=0.18.0',
            'requests>=2.0.0',
			'toml>=0.10' ,
			'pyzstd >=0.15',
			'numpy>=1.9.2'
            ]
    return reqs
setup(
	name = "dbpystream",
	version = get_version(),
    author ="songroom",
    author_email = "rustroom@163.com",
    long_description_content_type="text/markdown",
	url = 'https://github.com/songroom2016/dbpystream.git',
	long_description = open('README.md',encoding="utf-8").read(),
    python_requires=">=3.6",
    install_requires=get_install_requires(),
	packages = find_packages(),
 	license = 'Apache',
   	classifiers = [
       'License :: OSI Approved :: Apache Software License',
       'Natural Language :: English',
       'Operating System :: OS Independent',
       'Programming Language :: Python',       
       'Programming Language :: Python :: 3.6',
       'Topic :: Software Development :: Libraries :: Python Modules',
   ],
 
)
