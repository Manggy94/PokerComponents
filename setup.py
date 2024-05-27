from pathlib import Path
from setuptools import setup, find_packages
import json


install_requires = [        
    "parsedatetime",
    "cached-property",
    "numpy",
    "pandas",
    "pytest",
    "coverage",
    "pytest-cov",
    "attrs",
]

classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Natural Language :: French",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Topic :: Games/Entertainment",
    "Topic :: Games/Entertainment :: Board Games"
]


def get_version():
    with open("config/version.json", "r") as f:
        version = json.load(f)
        return f"{version['major']}.{version['minor']}.{version['patch']}"


setup(
    name="pkrcomponents",
    version=get_version(),
    description="A Poker Package",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    classifiers=classifiers,
    keywords="poker pkrcomponents pkr",
    author="Alexandre MANGWA",
    author_email="alex.mangwa@gmail.com",
    url="https://github.com/manggy94/PokerComponents",
    license="MIT",
    packages=find_packages(exclude=["tests", ".venv", "venv", "venv.*"]),
    install_requires=install_requires,
    tests_require=["pytest", "pytest-cov", "coverage", "coveralls"],
)
