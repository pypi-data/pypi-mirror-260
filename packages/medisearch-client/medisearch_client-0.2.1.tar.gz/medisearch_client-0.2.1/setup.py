"""Setup file for the medisearch_client package."""

from setuptools import setup, find_packages

setup(
    name="medisearch_client",
    version="0.2.1",
    packages=find_packages(),
    install_requires=[
        "websocket-client", "pyasn1", "pyopenssl", "ndg-httpsclient"
    ],
    author="Michal Pandy",
    author_email="founders@medisearch.io",
    description="A simple client for the MediSearch API",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MediSearch/medisearch_client_python",
)
