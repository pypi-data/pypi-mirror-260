from setuptools import find_namespace_packages, setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='regression_graph',
    version='0.1',
    description="Python library to create regression graphs",
    packages=find_namespace_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown", 
    author="Saema Khanom",
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        'numpy',
        'matplotlib',
        'statsmodels',
        'pandas',
    ],
)

