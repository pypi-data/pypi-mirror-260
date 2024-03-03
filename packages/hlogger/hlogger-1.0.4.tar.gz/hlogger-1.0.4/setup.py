import pathlib

from setuptools import setup, find_packages


here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="hlogger",
    version="1.0.4",
    description="A logger utility for python application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/llChameleoNll/hlogger",
    packages=find_packages(),
    package_dir={"hlogger": "src"},
    author="llChameleoNll",
    author_email="chameleon2318@gmail.com",
    keywords="logger, logging",
    python_requires="~=3.6",
    project_urls={
        "Bug Reports": "https://github.com/sChameleoNz/hlogger/issues",
        "Source": "https://github.com/sChameleoNz/hlogger",
        "Buy me a coffee": "https://www.buymeacoffee.com/llhoyall",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
