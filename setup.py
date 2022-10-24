from pathlib import Path
from setuptools import setup, find_packages


install_requires = [        
    "parsedatetime",
    "cached-property",
    "numpy",
    "pandas",
    "pytest",
    "coverage",
    "pytest-cov"
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

setup(
    name="pkrcomponents",
    version="0.0.1",
    description="A Poker Package",
    long_description=Path("README.rst").read_text(),
    classifiers=classifiers,
    keywords="poker pkrcomponents pkr",
    author="Alexandre MANGWA",
    author_email="alex.mangwa@gmail.com",
    url="https://github.com/manggy94/PokerComponents",
    license="MIT",
    packages=find_packages(),
    install_requires=install_requires,
    tests_require=["pytest", "pytest-cov", "coverage", "coveralls"],
)
