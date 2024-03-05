from setuptools import setup, find_packages

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()
setup(
    name="radars",
    version="0.0.1",
    author = "emteyaz",
    author_email = "emteyazalee@gmail.com",
    description = "Trying to publish something",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    packages=find_packages(),
    install_requires = [

    ],
)