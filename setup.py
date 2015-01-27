import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# Don't import analytics-python module here, since deps may not be installed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'shinchan'))

long_description = '''
ShinChan is a python project, which is a logging system build upon python's logging library,
it also helps in notifying critical logs to the developers via email
'''

setup(
    name='shinchan',
    packages = ['shinchan', 'shinchan.helper'],
    version= '0.0.1',
    url='https://github.com/asamat/shinchan',
    author='Arunim Samat',
    author_email='arunimsamat@gmail.com',
    license='MIT License',
    description='Logging and notification utility in python',
    long_description=long_description
)