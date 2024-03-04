from setuptools import setup
from setuptools_rust import Binding, RustExtension

setup(
    name="rustvdb",  # Use the name you want to publish on PyPI
    version="0.1.0",  # Increment this with each release
    rust_extensions=[RustExtension("rustvdb.rustvdb", binding=Binding.PyO3)],
    packages=["rustvdb"],  # This should match the Python package name inside your project
    # Specify any Python dependencies here. For example, if your package requires numpy,
    # add 'install_requires=["numpy>=1.19"]'
    install_requires=[],
    zip_safe=False,
    # Include additional metadata about your package
    author="Alan Newcomer",
    author_email="alan.b.newcomer@gmail.com",
    description="A Python module for managing and searching through high-dimensional embeddings, implemented in Rust.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",  # This assumes you have a README.md file
    url="https://github.com/alannewcomer/rustvdb",  # Link to your project repository
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    # Include any package data in a MANIFEST.in file or specify `package_data` parameter
    # package_data={"your_package": ["data/*.dat"]},
)
