import os
import stat

from setuptools import setup
from setuptools.command.install import install
from distutils import log

setup(
    name="pb-pip-test",
    version='1.0',
    packages=["pb-pip-test"],
    include_package_data=True,
    author='MarkLLM',
    author_email="projectmark.ai@gmail.com",
    description='Mark is an AI voice activated robot.',
    url="https://github.com/ProjectMarkLLM/pb-pip-test#readme",
    long_description='Mark is an AI voice activated robot powered using C++ and Python.',
    python_requires=">=3.8",
    install_requires=['requests>=2.26.0', "typing-extensions"]
)
