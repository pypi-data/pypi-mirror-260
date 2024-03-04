from setuptools import setup, find_packages
from pathlib import Path, PurePath


with open(PurePath(__file__).parent / "README.md") as f:
	long_description = f.read()

setup(
	name="pyrot13",
	version="0.1.0",
	author="Briano Goestiawan",
	author_email="b@briano.io",
	description="pyrot13 rotate letters by 13 place.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/bbriano/pyrot13",
	packages=find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"Operating System :: OS Independent",
		"License :: OSI Approved :: ISC License (ISCL)"
	],
	python_requires=">=3"
)
