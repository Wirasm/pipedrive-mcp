from setuptools import setup, find_packages

setup(
    name="mcp-concept",
    version="0.1.0",
    packages=find_packages(include=["pipedrive", "pipedrive.*"]),
)