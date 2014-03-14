#!/usr/bin/env python
"""
d3gem
-----

{description}
"""
import ast
from setuptools import setup


def read_tags(filename):
    """Reads values of "magic tags" defined in the given Python file.

    :param filename: Python filename to read the tags from
    :return: Dictionary of tags
    """
    with open(filename) as f:
        ast_tree = ast.parse(f.read(), filename)

    res = {}
    for node in ast.walk(ast_tree):
        if type(node) is not ast.Assign:
            continue

        target = node.targets[0]
        if type(target) is not ast.Name:
            continue

        if not (target.id.startswith('__') and target.id.endswith('__')):
            continue

        name = target.id[2:-2]
        res[name] = ast.literal_eval(node.value)

    return res


tags = read_tags('d3gem.py')
__doc__ = __doc__.format(**tags)


setup(
    name="d3gem",
    version=tags['version'],
    description=tags['description'],
    long_description=open('README.rst').read(),
    url='https://github.com/Xion/d3gem',
    author=tags['author'],
    license=tags['license'],

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
