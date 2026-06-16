from setuptools import setup, find_packages

setup(
    name="skillbridge-cv-analyzer",
    version="0.1.0",
    author="vinaydev00",
    description="NLP-powered semantic CV-to-Job matcher with Hidden Gem scoring",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "spacy>=3.7.0",
        "sentence-transformers>=2.7.0",
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "scikit-learn>=1.3.0",
        "rich>=13.0.0",
        "click>=8.1.0",
    ],
    entry_points={
        "console_scripts": [
            "skillbridge=src.main:analyze",
        ],
    },
)