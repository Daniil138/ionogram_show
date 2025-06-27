#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="ionogram_visualizer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'numpy>=1.21.0',
        'matplotlib>=3.5.0',
        'ionread_python'  
    ],
    author="Daniil",
    author_email="reetu",
    description="Library for ionogram visualization and processing",
    url="https://github.com/Daniil138/ionogram_show.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)