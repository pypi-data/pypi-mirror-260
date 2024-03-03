"""spmf - setup.py"""
from setuptools import setup, find_packages

LONG_DESC = open('README.md').read()

setup(
    name='spmf-wrapper',
    version='0.0.1',
    author='Aakash Vasudevan',
    author_email='Aakash.Vasudevan@gmail.com',
    description='Python Wrapper for SPMF',
    long_description_content_type='text/markdown',
    long_description=LONG_DESC,
    url='https://github.com/AakashVasudevan/Py-SPMF',
    include_package_data=True,
    packages=find_packages() + ['spmf/binaries'],
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3',
)
