import os

from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="pdeprecator",
    author="Prince Roshan",
    version='0.0.1',
    author_email="princekrroshan01@gmail.com",
    url="https://github.com/Agent-Hellboy/pdeprecator",
    description=("A library provides a decorator deprecated_params that allows you to deprecate certain parameters in your class methods or function."),
    long_description=read("README.rst"),
    license="MIT",
    package_dir={'': 'src'},
    packages=['pdeprecator'],
    keywords=[
        "deprecator","param-deprecator"
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
)