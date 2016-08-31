#!/usr/bin/env python

from setuptools import setup

with open('lazyscripts/version.py') as fid:
    for line in fid:
        if line.startswith('__version__'):
            version = line.strip().split()[-1][1:-1]
            break

setup(name='LazyScripts',
      packages=['LazyScripts'],
      version=version,
      description='Useful python modules for lazy scripting.',
      author='James Wenzel',
      author_email='wenzel.james.r@gmail.com',
      url='https://github.com/jameswenzel/LazyScripts',
      download_url='https://github.com/jameswenzel/LazyScripts/tarball/0.1.0',
      license='Apache License, Version 2.0',
      keywords=['lazy', 'csv', 'tor', 'multithread', 'beautifulsoup', 'json'],
      classifiers=[],
      install_requires=['beautifulsoup4 >= 4.4.1', 'requests >= 2.2.1',
                        'stem >= 1.4']
      )
