import os
from setuptools import find_packages, setup

with open("README.md", "r",encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='NFT-Mint-Wallet-Analysis',
    version='0.0.1',
    packages=find_packages(),
    long_description_content_type="text/markdown",
    long_description=long_description,

    author='Joey.C',
    author_email='molu0219@gmail.com',
    url='https://github.com/molu0219/NFT-Mint-Wallet-Analysis',
    keywords=[],
    classifiers=["Programming Language :: Python :: 3",
                 "Development Status :: 1 - Planning"],
    python_requires='>=3.7'

)
