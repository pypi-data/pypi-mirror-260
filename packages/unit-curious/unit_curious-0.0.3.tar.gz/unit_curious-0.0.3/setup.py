from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="unit_curious",
    version="0.0.3",
    description="Explore historical, quirky, and unconventional units of measurement with this easy-to-use Python library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
)
