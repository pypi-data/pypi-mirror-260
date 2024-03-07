from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="commitit",
    version="0.3",
    packages=find_packages(),
    description="It is not how good you are, it is about how good people think you are",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Didas G. Junior"
)
