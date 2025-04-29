from setuptools import setup, find_packages

setup(
    name="textstats",
    version="0.1.0",
    author="Sunny",
    author_email="sunny@example.com",
    description="A simple text statistics calculator",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sunny/textstats",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
