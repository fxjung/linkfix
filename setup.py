from setuptools import setup, find_packages
from os import path

ROOT_DIR = path.abspath(path.dirname(__file__))


with open(path.join(ROOT_DIR, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", "r") as f:
    reqs = f.readlines()

setup(
    name="linkfix",
    version="0.1",
    description="Fixes weblinks.",
    long_description=long_description,
    # url='',
    keywords="utilities, python",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
    ],
    packages=find_packages(),
    install_requires=reqs,
    author="Felix Jung",
    author_email="jung@posteo.de",
    # entry_points={"console_scripts": ["agent_smith = agent_smith.cli"]},
)
