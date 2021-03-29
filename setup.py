import setuptools

with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    name="argdeco-josugoar",
    version="1.4.0",
    description="Unopinionated argparse wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="josugoar",
    url="https://github.com/josugoar/argdeco",
    download_url="https://github.com/josugoar/argdeco/archive/v1.4.0.tar.gz",
    py_modules=["argdeco"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    package_data={"argdeco": ["LICENSE", "README.md"]},
    license="MIT",
    keywords="argparse cli library pipenv python wrapt",
    project_urls={"Source": "https://github.com/josugoar/argdeco"},
    install_requires=["wrapt"],
    python_requires=">=3.8"
)
