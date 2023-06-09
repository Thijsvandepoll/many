from setuptools import find_packages, setup

setup(
    name="many",
    version="0.0.1",
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
