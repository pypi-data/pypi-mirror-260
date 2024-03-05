from setuptools import setup, find_packages

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()
setup(
    name="radars",
    version="0.0.2",
    author = "emteyaz",
    author_email = "emteyazalee@gmail.com",
    description = "Trying to publish something",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    packages=find_packages(),
    install_requires = [

    ],
    url = "https://imtiyaz-ali.github.io/radars/",
    project_urls = {
        "Bug Tracker": "https://github.com/Imtiyaz-ali/radars/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
