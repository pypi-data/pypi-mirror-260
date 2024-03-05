#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

install_requires = [
    "boto3~=1.26.60",
    "PyPDF2~=2.10.9",
    "requests>=2.27.1",
    "datefinder~=0.7.1",
    "email-validator~=1.2.1",
    "usaddress~=0.5.10",
]

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
    install_requires=install_requires,
    keywords="t_ocr",
    name="t_ocr",
    packages=find_packages(include=["t_ocr", "t_ocr.*"]),
    test_suite="tests",
    url="https://www.thoughtfulautomation.com/",
    version="1.4.0",
    zip_safe=False,
)
