#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("requirements.txt") as requirements:
    install_requirements = requirements.readlines()

setup(
    author="Thoughtful",
    author_email="support@thoughtfulautomation.com",
    python_requires=">=3.8",
    classifiers=[
        "Intended Audience :: Automation Engineers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    description="Cookiecutter template for Thoughtful pip package",
    long_description=readme,
    include_package_data=True,
    install_requires=install_requirements,
    keywords="thoughtful-ocr, t-ocr, t_ocr",
    name="t_ocr",
    packages=find_packages(include=["t_ocr", "t_ocr.*"]),
    test_suite="tests",
    url="https://www.thoughtful.ai/",
    version="1.4.2",
    zip_safe=False,
)
