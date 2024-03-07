from setuptools import setup, find_packages
import codecs
import os



VERSION = '0.0.1'
DESCRIPTION = 'Mapping Pos Tags To Recognized WordNet Lemetaizer categories'
LONG_DESCRIPTION = 'A package that allows to Generate Recognized Pos Tags for WordNet Lemetaizer.'

# Setting up
setup(
    name="postagwordnet",
    version=VERSION,
    author="Michael Mansour",
    author_email="<michael.mansour@cis.asu.edu.eg>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['nltk>=3.5'],
    keywords=['python', 'nlp', 'nltk', 'pos-tag', 'mapping', 'wordnet','lemmatization'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)