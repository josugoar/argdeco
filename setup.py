import setuptools
from os import path

with open("README.md", encoding="utf8") as f:
    long_description = f.read()

setuptools.setup(
    name="argdeco-josugoar",
    version="1.3.1",
    description="Unopinionated argparse wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="josugoar",
    url="https://github.com/josugoar/argdeco",
    py_modules=["argdeco"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Basque",
        "Natural Language :: English",
        "Natural Language :: Spanish",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Topic :: Documentation",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    package_data={"argdeco": ["LICENSE", "README.md"]},
    license="MIT",
    keywords="python pip argparse wrapt",
    project_urls={"Source": "https://github.com/josugoar/argdeco"},
    install_requires=["wrapt"],
    python_requires=">=3.8"
)
