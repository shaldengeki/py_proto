from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="py_proto_parser",
    version="0.0.1",
    description="A Python protobuf parser library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shaldengeki/py_proto",
    author="Charles OuGuo",
    author_email="shaldengeki@gmail.com",
    classifiers=[ 
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="protobuf, protocol, buffers",
    package_dir={"": "src"},

    packages=find_packages(where="src"),
    python_requires=">=3.10, <4",
    install_requires=[], 
    entry_points={
        "console_scripts": [
            "parser=parser:main",
            "compatibility_checker=compatibility_checker:main",
        ],
    },
)