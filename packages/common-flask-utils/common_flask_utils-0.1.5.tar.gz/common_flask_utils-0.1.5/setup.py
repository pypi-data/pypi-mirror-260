from importlib.machinery import SourceFileLoader
from setuptools import setup, find_packages

version_module = SourceFileLoader(
    "version", "common_utils/version.py"
).load_module("version")

__version__ = version_module.__version__

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="common_flask_utils",
    version=__version__,
    author="Evanston Law",
    author_email="evanstonlaw555@gmail.com",
    url="https://github.com/Evan-acg/common_flask",
    description="Common Flask Utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["Flask", "Flask-SQLAlchemy", "python-i18n", "pyjwt", "flask-cors"],
    include_package_data=True,
    python_requires=">=3.10",
)
