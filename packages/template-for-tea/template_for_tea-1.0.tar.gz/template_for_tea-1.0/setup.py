# setup.py

import setuptools
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setuptools.setup(
    name="template_for_tea",
    version="1.0",
    author="Eminent",
    author_email="EminentGuXiang@protonmail.com",
    description="Template for project TEA.xyz,your gateway towards blockchain and OSS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eminentgu",
    packages=setuptools.find_packages(),
    license="Apache 2.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",

    ],
    keywords="template_for_tea",
)