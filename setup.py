import setuptools
from os import path

with open(path.join(path.dirname(__file__), "README.md"), encoding="utf8") as f:
    long_description = f.read()

setuptools.setup(
    name="argdeco",
    version="1.0.0",
    description="Unopinionated argparse wrapper",
    long_description=long_description,
    author="JoshGoA",
    url="https://github.com/JoshGoA/argdeco",
    py_modules=["argdeco"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Basque",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Build Tools"
    ],
    package_data={"argdeco": ["*.md", "*.txt"]},
    license="MIT",
    keywords="argparse wrapt",
    project_urls={"Source": "https://github.com/pypa/argdeco"},
    install_requires=["wrapt"],
    python_requires=">=3.8"
)
