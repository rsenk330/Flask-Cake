import os
import sys

from setuptools import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

with open("README.md", 'r') as readme_file:
    readme = readme_file.read()

setup(
    name='Flask-Cake',
    version='0.3.1',
    url='http://github.com/rsenk330/Flask-Cake',
    license='BSD',
    author='Ryan Senkbeil',
    author_email='me@ryansenkbeil.com',
    description='Flask extension to execute Cake on filesystem events.',
    long_description=readme,
    packages=['flask_cake'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask>=0.7',
        'six==1.6.1',
        'watchdog',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
