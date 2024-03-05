from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pychoreographer",
    version="0.0.4",
    description="A customizable Python library for automating file operations, system monitoring, and routine tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
)
