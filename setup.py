from setuptools import setup, find_packages

setup(
    name="gscraper",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        "selenium>=4.0",
        "beautifulsoup4>=4.9",
        "requests>=2.25",
        "aiohttp>=3.8",
    ],
    package_data={
        "gscraper": ["sample.gscraper"]
    },
    entry_points={
        "console_scripts": [
            "gscraper = gscraper:main",
        ],
    },
    author="Godfrey Enosh",
    author_email="godfreyenos360@gmail.com",
    description="A web scraper for extracting text and documents from websites",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Godie360/gscraper",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)