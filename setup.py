#!/usr/bin/env python
"""
d3gem -- Setup file
"""
from setuptools import setup


setup(
    name="d3gem",
    version="0.2.1",
    description="Diablo 3 gem crafting helper",
    long_description=open('README.rst').read(),
    url='https://github.com/Xion/d3gem',
    author='Karol Kuczmarski "Xion"',
    author_email='karol.kuczmarski@gmail.com',
    license="GPLv3",

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Games/Entertainment',
        'Topic :: Games/Entertainment :: Role-Playing',
        'Topic :: Utilities',
    ],

    platforms='any',
    entry_points={
        'console_scripts': ['d3gem=d3gem:main'],
    },
)
