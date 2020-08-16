import setuptools
from os import path

with open(path.join(path.dirname(__file__), "README.md")) as f:
    long_description = f.read()

setuptools.setup(
    name="argdeco",
    version="0.9.0",
    description="Stylish Decorator Syntax For Argparse",
    long_description=long_description,
    author="JoshGoA",
    url="https://github.com/JoshGoA/argdeco",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Basque",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Build Tools",
        "Typing :: Typed"
    ],
    package_data={"argdeco": ["*.md", "*.txt"]},
    license="MIT",
    keywords="argparse wrapt",
    project_urls={"Source": "https://github.com/pypa/argdeco"},
    install_requires=["wrapt"],
    python_requires=">=3.8"
)
