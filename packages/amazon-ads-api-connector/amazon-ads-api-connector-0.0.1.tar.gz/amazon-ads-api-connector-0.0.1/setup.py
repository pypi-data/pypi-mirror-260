from setuptools import setup, find_packages

setup(
    name="amazon-ads-api-connector",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "requests",
        "types-requests",
    ],
)
