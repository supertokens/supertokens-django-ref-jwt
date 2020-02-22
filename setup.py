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
        'jsonschema',
        'flake8',
        'autopep8'
    ])
}

setup(
    name="supertokens_jwt_ref",
    version="2.0.0",
    author="Bhumil Sarvaiya, Rishabh Poddar",
    license="MIT",
    author_email="sarvaiyabhumil@gmail.com, rishabh@supertokens.io",
    description="SuperTokens session management solution",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/supertokens/supertokens-django-ref-jwt",
    packages=find_packages(exclude=["contrib", "docs", "tests*", "licenses", "requirements"]),
    classifiers=[
        "Framework :: Django :: 2.2",
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Session",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="",
    install_requires=[
        "django",
        "djangorestframework",
        "pycryptodome",
    ],
    python_requires='>=3.7',
    extras_require=extras_require
)
