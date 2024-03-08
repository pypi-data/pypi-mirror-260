from setuptools import find_packages, setup
import os

version: str = "1.0.0"
description: str = "CLI tool for getting the web result from commandline"
long_description: str = (
    "A CLI tool for getting the result of web through terminal. Access Google Gemini AI through your terminal with an easy to install tool."
)

# Setting Up
setup(
    name="searchify-cli",
    version=version,
    author="Vishnu Tiwari aka dockvulner",
    author_email="<vishnutiwari728@gmail.com>",
    long_description=long_description,
    packages=find_packages("Web"),
    install_requires=[
        "cachetools",
        "certifi",
        "charset-normalizer",
        "google-ai-generativelanguage",
        "google-api-core",
        "google-auth",
        "google-generativeai",
        "googleapis-common-protos",
        "grpcio",
        "grpcio-status",
        "idna",
        "proto-plus",
        "protobuf",
        "pyasn1",
        "pyasn1-modules",
        "pyperclip",
        "python-dotenv",
        "requests",
        "rsa",
        "tqdm",
        "typing_extensions",
        "urllib3",
    ],
    keywords=[
        "python",
        "cli-python-tool",
        "web terminal",
        "commandline browser",
        "ai-search",
        "api-search",
    ],
    entry_points={
        "console_scripts": [
            "search = Web.main:main",
            "search-config = install:main",
            "ai-search= AI_Search.ai_search:main",
        ]
    },
)
