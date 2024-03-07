"""
Setup script for installing vecflowApi package.
"""

from setuptools import setup, find_packages

setup(
    name="vecflowApi",
    version="0.3.5",
    packages=find_packages(exclude=["tests", "tests.*", "docs", "docs.*"]),
    install_requires=["requests", "werkzeug"],
    # Metadata
    author="VecFlow Team",
    description="API wrapper for the VecFlow API",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/VecFlow/VecFlow",
    # More metadata
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
