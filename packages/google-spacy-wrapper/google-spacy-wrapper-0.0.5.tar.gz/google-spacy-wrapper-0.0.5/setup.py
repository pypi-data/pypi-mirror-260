from setuptools import setup, find_packages

VERSION = '0.0.5'
DESCRIPTION = 'Google Natural Language API Wrapper for Spacy'
LONG_DESCRIPTION = ''

# Setting up
setup(
    name="google-spacy-wrapper",
    version=VERSION,
    author="PySlayer (Paul Antweiler)",
    author_email="antweiler.paul@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['google-cloud-language'],
    keywords=['python', 'nlp', 'natural language', 'google', 'google cloud', 'spacy', 'wrapper'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)