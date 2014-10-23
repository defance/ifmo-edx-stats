import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='ifmo-edx-stats',
    version='0.1',
    packages=['ifmo_stats'],
    include_package_data=True,
    license='BSD License',
    description='Package provides stats for courses.',
    long_description=README,
    url='http://www.de.ifmo.ru/',
    author='Nikita Vasilev',
    author_email='dnfletter@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License', 
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
