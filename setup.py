from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="langchain-querit",
    version="0.0.2",
    author="Your Name",
    author_email="your-real-email@example.com",
    description="A LangChain tool for Querit search functionality",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KKKPJSKEY/langchain-querit",
    keywords=["langchain", "websearch", "querit", "search-tool"],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "langchain>=0.0.300",
        "pydantic>=1.10.0",
        "requests>=2.28.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "types-requests",  # Type stubs for requests library
        ],
    },
    include_package_data=True,
)