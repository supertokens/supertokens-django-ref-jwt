from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), mode="r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name = "supertokens_session",
    verion = "0.0.1",
    author = "Bhumil Sarvaiya",
    author_email = "sarvaiyabhumil@gmail.com",
    description = "Supertokens package for python (DRF)",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    # url = "https://github.com/...",
    packages = find_packages(exclude=["contrib", "docs", "tests*", "tests", "licenses", "requirements"]),
    classifiers = [
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools :: Session Management",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # project_urls = {
    #     "Documentation": "https://packaging.python.org/tutorials/distributing-packages/",
    #     "Funding": "https://donate.pypi.org",
    #     "Say Thanks!": "http://saythanks.io/to/example",
    #     "Source": "https://github.com/pypa/sampleproject/",
    #     "Tracker": "https://github.com/pypa/sampleproject/issues",
    # },
    keywords = "",
    install_requires = [
        "django",
        "djangorestframework",
        "pyjwt",
    ],
    python_requires='>=3.7'
)