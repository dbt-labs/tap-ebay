#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='tap-ebay',
      version='0.0.1',
      description='Singer.io tap for extracting data from the Ebay API',
      author='Fishtown Analytics',
      url='http://fishtownanalytics.com',
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      py_modules=['tap_ebay'],
      install_requires=[
          'tap-framework==0.1.1',
      ],
      entry_points='''
          [console_scripts]
          tap-ebay=tap_ebay:main
      ''',
      packages=find_packages(),
      package_data={
          'tap_ebay': [
              'schemas/*.json'
          ]
      })
