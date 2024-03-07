import sys
import os

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == "publish":
    os.system("python3 setup.py sdist upload -r pypi")
    sys.exit()
elif len(sys.argv) == 1:
    print("Usage: python setup.py <command>")
    print("Available commands: publish")
    sys.exit()

with open("requirements.txt", encoding="utf-8") as f:
    required_packages = f.read().splitlines()

setup(
    name="chaintech",
    version="1.0.0",
    author="Chaintech",
    packages=find_packages(),
    install_requires=required_packages,
    include_package_data=True,
)
