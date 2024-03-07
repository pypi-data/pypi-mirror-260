from setuptools import setup, find_packages

VERSION = "1.0.4"
DESCRIPTION = "Piaget's FUCs filler"
LONG_DESCRIPTION = ''

setup(
    name="pyaget-fucs",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Natanael Quintino",
    author_email="natanael.quintino@ipiaget.pt",
    license='CC0 1.0 Universal',
    packages=find_packages(
        include=['pyaget_fucs', 'pyaget_fucs.*']
        ),
    install_requires=[
        "pdflatex", "langchain_openai"
    ],
    keywords='automation, curricular unit, FUC, piaget',
    classifiers= [
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ]
)
