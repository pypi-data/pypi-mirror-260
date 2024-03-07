# setup.py

from setuptools import setup, find_packages

setup(
    name='dalhelper',
    version='0.6',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[],
)
