from setuptools import setup, find_packages

setup(
    name="llm_helpers",
    version="0.1",
    packages=find_packages(),
    description="A helper package to work with LLMs",
    author="Sonny Laskar",
    author_email="sonnylaskar@gmail.com",
    keywords="llm",
    url="https://github.com/sonnylaskar/llm_helpers",
    install_requires=[
        "langchain_openai",  # Specify the version if necessary, e.g., "langchain_openai>=1.0"
        "langchain",  # Specify the version if necessary, e.g., "langchain>=1.0"
        # Since re and json are part of the standard library, they are not included here.
    ],
    python_requires='>=3.9',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
