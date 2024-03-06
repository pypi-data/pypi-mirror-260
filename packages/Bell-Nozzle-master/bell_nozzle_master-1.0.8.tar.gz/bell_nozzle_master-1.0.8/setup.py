#!/usr/bin/env python
"""Install minimal requirements."""

import codecs
import os
from setuptools import setup, find_packages


# these things are needed for the README.md show on pypi
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()


VERSION = '1.0.5'
DESCRIPTION = 'Tools for designing bell nozzles'
LONG_DESCRIPTION = 'Tools for designing bell nozzles'

dev_requirements = [
    "tox==3.14.2",
    "pytest==5.3.2",
    "pytest-mock==1.13.0",
    "pytest-cov==2.8.1",
    "pytest-sugar==0.9.2",
    "black==20.8b1",
    "flake8==3.8.3",
    "requests_mock==1.7.0",
    "therapist==2.1.0",
]

# Setting up
setup(
    name="Bell-Nozzle-master",
    version=VERSION,
    author="",
    author_email="",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(include=["Bell-Nozzle-master", "Bell-Nozzle-master.*"], ),
    install_requires=[
        'docutils',
        'BazSpam ==1.1',
        'requests>=2.25.1',
        'numpy>=1.21.2',
        'pandas>=1.3.2',
    ],
    extras_require={"dev": dev_requirements},
    keywords=['python','nozzle','bell nozzle'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-mock", "requests_mock"]
)