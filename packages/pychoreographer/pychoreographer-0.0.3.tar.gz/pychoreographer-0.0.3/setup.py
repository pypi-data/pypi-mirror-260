from setuptools import setup, find_packages

setup(
    name="pychoreographer",
    version="0.0.3",
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
)
