#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='yad2parser',
      version='1.0',
      description='parser for standAlone',
      author='Gad avivi',
      author_email='gadavivi@gmail.com',
      packages=find_packages(),
      install_requires=['request']
     )