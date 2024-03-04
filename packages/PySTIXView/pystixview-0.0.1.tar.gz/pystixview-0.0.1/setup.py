from setuptools import setup, find_packages

VERSION_FILE = "pystixview/_version.py"

exec(open(VERSION_FILE).read())

setup(
    name="PySTIXView",
    version=__version__,
    description="A Python library to create and display STIX2 graphs.",
    url="https://github.com/vincenzocaputo/PySTIXView",
    author="Vincenzo Caputo",
    license="BSD",
    packages=find_packages(),
    install_requires=[
        "pyvis >= 0.3.2",
        "stix2 >= 3.0.1"
    ],
)
