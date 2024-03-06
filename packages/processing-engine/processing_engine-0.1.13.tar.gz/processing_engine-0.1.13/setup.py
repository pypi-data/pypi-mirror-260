#!/usr/bin/env python
import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "processing_engine",
    version = "0.1.13",
    author = "Anonym Drifter",
    description = ("Processing Engine for Data Driven Analytics"),
    license = "GNU",
    keywords = "Processing Engine",
    packages=['processing_engine', 'tests'],
    long_description="None",
    classifiers=[
        "Development Status :: 3 - Alpha",
    ],
)
