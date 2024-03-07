#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "Click>=7.0",
    "Rich",
    "PyYAML"
]

test_requirements = []

setup(
    author="Jaideep Sundaram",
    author_email="jai.python3@gmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Package for parsing a tab-delimited data file and loading the lines into SQLite3 database",
    entry_points={
        "console_scripts": [
            "csv2sqlite=tsv2sqlite.csv2sqlite:main",
            "tsv2sqlite=tsv2sqlite.main:main",
            "add-header-row=tsv2sqlite.add_header_row:main",
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="tsv2sqlite",
    name="tsv2sqlite",
    packages=find_packages(include=["tsv2sqlite", "tsv2sqlite.*"]),
    package_data={"tsv2sqlite": ["conf/config.yaml"]},
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/jai-python3/tsv2sqlite",
    version="0.4.0",
    zip_safe=False,
)
