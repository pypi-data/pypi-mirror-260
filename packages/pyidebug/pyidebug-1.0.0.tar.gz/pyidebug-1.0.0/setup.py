from setuptools import setup, find_packages

VERSION = "1.0.0"
DESCRIPTION = "Module that allows you to interactively debug your code."
LONG_DESCRIPTION = ''

setup(
    name="pyidebug",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Natanael Quintino",
    author_email="natanael.quintino@ipiaget.pt",
    license='CC0 1.0 Universal',
    packages=find_packages(
        include=['pyidebug', 'pyidebug.*']
        ),
    install_requires=[        
    ],
    keywords='debug, interactive, edit, code',
    classifiers= [
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ]
)
