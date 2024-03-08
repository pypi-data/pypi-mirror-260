#!/usr/bin/env python

"""The setup script."""
from pathlib import Path
from setuptools import setup, find_packages



here = Path(__file__).resolve().parent
long_description = (here / "README.md").read_text(encoding="utf-8")
requirements = (here / "requirements.txt").read_text(encoding="utf-8").splitlines()


test_requirements = ['pytest>=3', ]

setup(
    author="fengyunzaidushi",
    author_email='fengxiaoyang163@163.com',
    python_requires='>=3.10',
    description="ai effiency tool",
    entry_points={
        'console_scripts': [
            'aiefftool=aiefftool.cli:main',
        ],
    },
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='aiefftool',
    name='aiefftool',
    packages=find_packages(include=['aiefftool', 'aiefftool.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/fengyunzaidushi/aiefftool',
    version='0.1.0',
    zip_safe=False,
)
