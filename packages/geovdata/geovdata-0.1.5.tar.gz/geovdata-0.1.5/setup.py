from setuptools import setup, find_packages

f = open("./version.txt", 'r')
versions = f.read()
f.close()

setup(
    name="geovdata",
    version=versions,
    author='Gaétan Muck',
    author_email='gaetan.muck@kleiolab.com',
    description='Package with various python tools',
    long_description='Package with various python tools created to help analysis on Geovistory and other SPARQL endpoints.',
    packages=find_packages(),
    install_requires=[
        "pandas",
        "gmpykit",
        "SPARQLWrapper"
    ],
    keywords=['python', 'toolkit', 'utilities', 'utils', 'tools', 'sparql']
)