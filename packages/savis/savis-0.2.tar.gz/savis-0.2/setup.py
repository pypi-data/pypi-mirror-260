from setuptools import setup, find_packages

setup(
    name="savis",
    version="0.2",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "transformers>=4.0.0",
        "matplotlib",
        "torch>=1.7.1"
    ],
    author="Seongbum Seo",
    author_email="seo@seongbum.com",
    description="A Sentence-Level Visualization of Attention in Transformers",
    keywords="text generation visualization transformers",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)
