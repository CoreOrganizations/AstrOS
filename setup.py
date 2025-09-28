#!/usr/bin/env python3
"""
AstrOS setup script
"""
from setuptools import setup, find_packages

setup(
    name="astros",
    version="1.0.0",
    description="AI-First Operating System Assistant powered by GPT-OSS-20B",
    author="AstrOS Team",
    author_email="team@astros.org",
    url="https://github.com/CoreOrganizations/AstrOS",
    
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    
    install_requires=[
        "openai>=1.0.0",
        "tiktoken>=0.5.0", 
        "httpx>=0.24.0",
        "pydantic>=2.5.0",
        "pyyaml>=6.0",
        "click>=8.1.0",
        "spacy>=3.7.0",
        "scikit-learn>=1.3.0",
        "numpy>=1.22.0",
    ],
    
    extras_require={
        "dev": ["pytest>=7.0.0", "black", "flake8"],
    },
    
    entry_points={
        "console_scripts": [
            "astros=astros.cli:cli",
        ],
    },
    
    python_requires=">=3.10",
    
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)