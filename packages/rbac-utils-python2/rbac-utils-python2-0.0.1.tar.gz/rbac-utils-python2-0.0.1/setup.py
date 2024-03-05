""" Utilities for RBAC system """

from setuptools import setup, find_packages

setup(
    name='rbac-utils-python2',
    version='0.0.1',
    description='Utilities for RBAC system',
    author='Sandeep Sharma',
    author_email='sandeep.sharma@lendenclub.com',
    url='',
    packages=find_packages(),
    install_requires=[
        'PyJWT==1.7.1',
        'requests==2.18.4',
        'python-dotenv==0.18.0'
    ]
)
