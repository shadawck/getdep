# !/usr/bin/env python3

import pathlib
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

# test dependencies
test_deps = [
    'pytest',
    'pytest-cov',
]
extras = {
    'test': test_deps,
}

# This call to setup() does all the work
setup(
    name="getdep",
    version="1.1.1",
    description="Get dependencies for a given package management system and a given package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/remiflavien1/getdep",
    author="shadawck",
    author_email="hug211mire@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        'Topic :: Security',
        'Topic :: Security :: Cryptography'
    ],
    packages=["getdep"],
    include_package_data=True,
    install_requires=["requests"],
    keywords='security, dependencies, package management, dependencies manager',
    tests_require=test_deps,
    extras_require=extras
)