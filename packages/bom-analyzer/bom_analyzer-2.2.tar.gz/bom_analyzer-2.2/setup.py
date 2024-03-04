from setuptools import setup, find_packages

VERSION = '2.2'

description = open("README.md", "r")

setup(
    name='bom_analyzer',
    version= VERSION,
    description='Bill of Materials outlier analysis using unsupervised machine learning.',
    long_description="README.md",
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