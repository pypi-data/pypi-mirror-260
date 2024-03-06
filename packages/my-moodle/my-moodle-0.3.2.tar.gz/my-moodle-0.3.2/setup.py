"""
Copyright © 2024 Mark Crowe <https://github.com/marcocrowe>. All rights reserved.
Setuptools configuration for my-moodle package.
"""

from setuptools import setup, find_packages

setup(
    name="my-moodle",
    version="0.3.2",
    author="Mark Crowe",
    author_email="66536097+marcocrowe@users.noreply.github.com",
    description="Download Moodle Course content.",
    long_description=open("readme.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/marcocrowe/my-moodle-py-pi/",
    project_urls={"Bug Tracker": "https://github.com/marcocrowe/my-moodle-py-pi/issues"},
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9"
)
