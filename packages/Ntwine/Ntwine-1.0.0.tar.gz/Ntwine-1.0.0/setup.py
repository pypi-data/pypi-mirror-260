from setuptools import setup
import os

location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
readme_loc = os.path.join(location, 'README.md')

long_description = open(readme_loc).read()
setup(name="Ntwine",
version="1.0.0",
description="Upload pypi package using termux by Ntwine .",
long_description=long_description,
long_description_content_type='text/markdown',
author="CodingSangh",
py_modules=[],
url="https://github.com/CodingSangh/Ntwine",
scripts=["Ntwine"],
install_requires= ['requests'],
classifiers=[
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
], )
