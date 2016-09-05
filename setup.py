#!/usr/bin/env python

from setuptools import setup


def load_version(path):
    with open(path) as fid:
        for line in fid:
            if line.startswith('__version__'):
                version = line.strip().split('=')[-1][1:-1]
                return version

# for some reason, "try" fails on linux, but "except"
# fails on mac os
try:
    version = load_version('lazyscripts/version.py')
except:
    version = load_version('LazyScripts/version.py')

setup(name='LazyScripts',
      packages=['LazyScripts'],
      version=version,
      description='Useful python modules for lazy scripting.',
      author='James Wenzel',
      author_email='wenzel.james.r@gmail.com',
      url='https://github.com/jameswenzel/LazyScripts',
      download_url=('https://github.com/jameswenzel/LazyScripts/tarball/'
                    '{0}'.format(version)),
      license='Apache License, Version 2.0',
      keywords=['lazy', 'csv', 'tor', 'multithread', 'beautifulsoup', 'json'],
      classifiers=[],
      install_requires=['beautifulsoup4 >= 4.4.1', 'requests >= 2.2.1',
                        'stem >= 1.4']
      )
