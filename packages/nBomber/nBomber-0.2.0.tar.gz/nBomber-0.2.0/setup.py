from setuptools import setup
import os

location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
readme_loc = os.path.join(location, 'README.md')

long_description = open(readme_loc).read()
setup(name="nBomber",
version="0.2.0",
description="SMS BOMBING TOOL WITH HAVING 50,000 MESSAGE SENDING CAPACITY AT A TIME.",
long_description=long_description,
long_description_content_type='text/markdown',
author="CodingSangh",
py_modules=['setup'],
url="https://github.com/CodingSangh/nBomber",
scripts=["nBomber"],
install_requires= ['certifi>=2020.6.20', 'chardet>=3.0.4', 'colorama>=0.4.3', 'idna>=2.10', 'requests>=2.24.0'],
classifiers=[
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
], )
