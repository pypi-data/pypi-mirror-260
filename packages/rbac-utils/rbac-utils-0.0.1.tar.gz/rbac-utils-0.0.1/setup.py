""" Utilities for RBAC system """

from setuptools import setup, find_packages

setup(
    name='rbac-utils',
    version='0.0.1',
    description='Utilities for RBAC system',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Sandeep Sharma',
    author_email='sandeep.sharma@lendenclub.com',
    url='',
    packages=find_packages(),
    install_requires=[
        'PyJWT==2.7.0',
        'requests==2.18.4',
        'python-dotenv==1.0.0'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.8',
    ],
)
