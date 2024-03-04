from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="roothazardlib",
    version="1.7",
    author="roothazard",
    description="Development tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dkushche/RHLib_Python3",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "pydantic>=2.5.3",
        "PyYAML>=6.0.0"
    ],
)
