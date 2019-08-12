from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), mode="r", encoding="utf-8") as f:
    long_description = f.read()

extras_require = {
    'dev': ([
        'pytest',
        'pytest-django',
        'jsonschema'
    ])
}

setup(
    name = "supertokens_session",
    verion = "0.0.1",
    author = "Bhumil Sarvaiya",
    author_email = "sarvaiyabhumil@gmail.com",
    description = "Supertokens package for python (DRF)",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/supertokens/supertokens-django-ref-jwt",
    packages = find_packages(exclude=["contrib", "docs", "tests*", "tests", "licenses", "requirements"]),
    classifiers = [
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools :: Session Management",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords = "",
    install_requires = [
        "django",
        "djangorestframework",
        "pycryptodome",
    ],
    python_requires='>=3.7',
    extras_require=extras_require
)