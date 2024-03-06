import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="dbpipe",
    version="0.2.0",
    description="Lightweight DataPipeline Documentation",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/jrasband-dev/dbpipe",
    author="Jayden Rasband",
    author_email="jayden.rasband@gmail.com",
    license="MIT",
    classifiers=[],
    packages=["dbpipe"],
    include_package_data=True,
    install_requires=[],
)