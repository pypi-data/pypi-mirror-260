from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.2.2'
DESCRIPTION = 'Get quotes wrapper'
LONG_DESCRIPTION = 'A package that allows to get Quotes from api-ninjas.com.'

# Setting up
setup(
    name="quotesgeneratorapi-wrapper",
    version=VERSION,
    author="tct123 <42028373+tct123@users.noreply.github.com>",
    author_email="<tct1234@protonmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'wrapper', 'api', 'quotes'],
    classifiers=[]
)
