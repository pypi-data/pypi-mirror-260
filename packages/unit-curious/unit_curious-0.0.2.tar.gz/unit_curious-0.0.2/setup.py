from setuptools import setup, find_packages

setup(
    name="unit_curious",
    version="0.0.2",
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
)
