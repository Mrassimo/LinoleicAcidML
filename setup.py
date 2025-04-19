from setuptools import setup, find_packages

setup(
    name="seedoilsml",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "scikit-learn",
        "matplotlib",
        "seaborn",
        "pydantic",
        "pytest",
        "sentence-transformers",
        "openpyxl",
        "requests",
        "beautifulsoup4",
    ],
) 