from setuptools import setup, find_packages

setup(
    name="bincat",
    version="2.0.0",
    description="Token generator and validator for authentication",
    author="Edu Olivares",
    packages=find_packages(),
    install_requires=[
        "colorama==0.4.4",
    ],
)
