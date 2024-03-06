from setuptools import setup, find_packages

# Read the contents of your README file
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="llm_helpers",
    version="0.1.1",
    packages=find_packages(),
    description="A helper package to work with LLMs",
    long_description=long_description,
    long_description_content_type='text/markdown',  # This is important!
    author="Sonny Laskar",
    author_email="sonnylaskar@gmail.com",
    keywords="llm",
    url="https://github.com/sonnylaskar/llm_helpers",
    install_requires=[
        "langchain_openai",
        "langchain",
        # Note: 're' and 'json' are part of the standard library, so they're not listed here.
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
