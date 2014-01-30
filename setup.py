#!/usr/bin/env python
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages


setup(name='Koemei API Client',
      version='1.0',
      description='Koemei Client - search and transcribe',
      author='Koemei',
      author_email='dev@koemei.com',
      url='https://www.koemei.com',
      packages=find_packages(exclude=['ez_setup']),
      include_package_data=True,
      package_data={'koemei': ['*/*/*/*/*/*']},
      license='Apache License 2.0',
      keywords='Koemei python transcription captions search video education',
      install_requires=[
          "requests >=2.0.0",
          "progressbar >= 2.2"
      ],
 )