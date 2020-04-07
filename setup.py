import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# This call to setup() does all the work
setup(
    name="getdep",
    version="1.0.0",
    description="Get dependencies for a given package management system and a given package.",
    long_description="README.md",
    long_description_content_type="text/markdown",
    url="https://github.com/remiflavien1/getdep",
    author="Rémi HUGUET - fractalizer",
    author_email="hug211mire@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["scabi"],
    include_package_data=True,
    install_requires=["requests", "json", "shlex", "subprocess"],
    entry_points={
        "console_scripts": [
            "scabi=scabi.__main__:main",
        ]
    },
)