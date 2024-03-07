from setuptools import setup, find_packages

setup(
    name="smart-manage-crypt",
    version="0.0.2b0",
    packages=find_packages(),
    install_requires=["pycryptodome==3.20.0"],
    python_requires=">=3.10",
)
