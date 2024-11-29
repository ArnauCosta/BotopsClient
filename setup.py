from setuptools import setup, find_packages

setup(
    name="botops",  # Package name
    version="0.1.0",
    description="A Python client for interacting with the BotOps API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Arnau Costa",
    author_email="arnaucosta23@gmail.com",
    url="https://github.com/ArnauCosta/BotopsClient",  # Repository URL
    packages=find_packages(),  # Automatically find sub-packages
    install_requires=["requests", "pydantic"],  # List dependencies
    python_requires=">=3.7",
    license="Apache License 2.0",  # License type
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
