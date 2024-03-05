from setuptools import setup, find_packages

VERSION = '2.3'

file = open("README.md", "r")
description = file.read()

setup(
    name='bom_analyzer',
    version= VERSION,
    description='Bill of Materials outlier analysis using unsupervised machine learning.',
    long_description=description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'sentence_transformers',
        'matplotlib',
        'umap-learn',
        'hdbscan',
        'scikit-learn',
        'optuna',
        'tqdm'
    ]
)