from setuptools import setup, find_packages
import sys
import os

version = '0.0.2'

setup(name='s3compress',
      version=version,
      description="compress files on s3 prefix",
      classifiers=[],
      keywords='s3 compress',
      author='Padmakar Ojha',
      author_email='padmakarojha@gmail.com',
      url='https://pip.pypa.io/',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=["click", "future", "boto"],
      entry_points={
          'console_scripts': [
              's3compress = s3compress.main:main',
          ]
      },
      )
