import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="HTBClient",
    version="0.2.3",
    author="Benjamin Grewell",
    author_email="bgrewelldev@gmail.com",
    description="A command line client and library to interact with the hackthebox.eu website",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BGrewell/HTBClient",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
        "Natural Language :: English",
        "Environment :: Console",
        "Intended Audience :: Information Technology",
    ],
    entry_points={
        'console_scripts': [
            'htb=HTBClient.__main__:main'
        ]
    },
    python_requires='>=3.6',
)
