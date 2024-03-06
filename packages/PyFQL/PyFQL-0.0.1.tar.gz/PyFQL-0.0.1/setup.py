import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyFQL",
    version="0.0.1",
    author="Banas Yann",
    author_email="yannbanas@gmail.com",
    description="A simple french query language for keysdb.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yannbanas/PyFQL",
    packages=setuptools.find_packages(where="src"),
    package_dir = {"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
