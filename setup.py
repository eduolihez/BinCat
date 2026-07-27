from setuptools import setup, find_packages

setup(
    name="bincat",
    version="2.0.0",
    description="Secure Token generation and validation SDK with database management",
    author="Edu Olivares",
    packages=find_packages(),
    install_requires=[
        "colorama>=0.4.6",
        "cryptography>=46.0.5",
        "python-dotenv>=1.0.1",
        "Flask>=3.0.3",
        "PyJWT>=2.8.0",
    ],
)
