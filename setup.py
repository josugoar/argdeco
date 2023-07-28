import setuptools

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="argdeco-josugoar",
    version="1.6.0",
    description="Opinionated argparse wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="josugoar",
    url="https://github.com/josugoar/argdeco",
    download_url="https://github.com/josugoar/argdeco/archive/v1.6.0.tar.gz",
    py_modules=["argdeco"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    package_data={"argdeco": ["LICENSE", "README.md", "py.typed", "argdeco.pyi"]},
    license="MIT",
    keywords="argparse cli docker library python",
    project_urls={"Source": "https://github.com/josugoar/argdeco"},
    python_requires=">=3.9"
)
