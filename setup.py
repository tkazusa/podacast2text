# -*- coding: UTF-8 -*-
from setuptools import setup, find_packages


setup(
    name='podcast2text',
    version='0.1',
    author='Taketoshi Kazusa',
    author_email='takekazusa@gmail.com',
    install_requires=['flask'],
    url='https://github.com/tkazusa/podcast2text.git',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    extras_require={
        'test': [
            'pytest',
            'coverage',
        ],
    }
)
