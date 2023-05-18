from setuptools import setup

setup(
    name="quintus",
    version="0.2",
    description="Document Embedding and Inference",
    author="rjmacarthy",
    author_email="rjmacarthy@protonmail.com",
    url="https://github.com/rjmacarthy/quintus",
    package_dir={"": "src"},
    install_requires=[
        "beautifulsoup4",
        "pgvector",
        "json",
        "numpy",
        "pathlib",
        "pydash",
        "sentence-transformers",
        "spacy",
        "torch",
        "tqdm",
        "unittest",
        "openai",
    ],
)
