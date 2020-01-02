import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="HTBClient",
    version="0.1.0",
    author="Benjamin Grewell",
    author_email="bgrewelldev@gmail.com",
    description="A library to interact with the hackthebox.eu website",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BGrewell/HTBClient",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)