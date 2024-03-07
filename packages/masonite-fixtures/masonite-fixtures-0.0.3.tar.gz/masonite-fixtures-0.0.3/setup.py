from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="masonite-fixtures",
    version="0.0.3",
    author="Jarriq Rolle",
    author_email="jrolle@bnbbahamas.com",
    description="Package provides utilities for managing fixture data python applications. It offers a convenient way to populate database tables with predefined data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JarriqTheTechie/masonite-fixtures",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=[
        "masonite-orm"
    ],
)
