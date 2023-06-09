import tomli
from setuptools import find_packages, setup

# Read the version from pyproject.toml
version = None
with open("pyproject.toml", "rb") as fp:
    pyproject_toml = tomli.load(fp)
    version = pyproject_toml["tool"]["poetry"]["version"]

setup(
    name="many-migrations",
    version=version,
    description="A library to create a customized migration application.",
    author="Thijs van de Poll",
    author_email="thijsvandepoll@gmail.com",
    license="MIT Licence",
    include_package_data=True,
    keywords="migrations, migration library, many, custom",
    packages=find_packages(where="src"),
    long_description="README.md",
    package_dir={"": "src"},
)
