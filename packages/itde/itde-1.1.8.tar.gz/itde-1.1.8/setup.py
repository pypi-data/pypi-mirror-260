from setuptools import find_packages  # type: ignore
from setuptools import setup
from pathlib import Path


here = Path(__file__).parent
long_description = (here / "README.md").read_text()


setup(
    name="itde",
    version="1.1.8",
    description="InnerTube Data Extractor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Simone Gentili (g3nsy)",
    author_email="",
    python_requires=">=3.6.0",
    url="https://github.com/g3nsy/itde",
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    install_requires=[],
    include_package_data=True,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
