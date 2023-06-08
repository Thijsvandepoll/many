# setup.py
from setuptools import find_packages, setup

setup(
    name="many",
    version="0.1",
    description="Package to create customized migrations.",
    author="Thijs van de Poll",
    author_email="thijsvandepoll@gmail.com",
    license="MIT Licence",
    include_package_data=True,
    keywords="migrations, migration package, many",
    packages=find_packages(where="src"),
    long_description="README.md",
    package_dir={"": "src"},
)
