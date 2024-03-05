import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sdkgen-client",
    version="0.1.0",
    author="Christoph Kappestein",
    author_email="christoph.kappestein@gmail.com",
    description="SDKgen client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/apioo/sdkgen-python",
    packages=["sdkgen"],
    package_data={"": ["LICENSE"]},
    package_dir={"": "src"},
    include_package_data=True,
    python_requires='>=3',
    install_requires=[
        "requests",
        "dataclasses-json"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Code Generators"
    ],
    tests_require=[
        "pytest>=3"
    ],
)
