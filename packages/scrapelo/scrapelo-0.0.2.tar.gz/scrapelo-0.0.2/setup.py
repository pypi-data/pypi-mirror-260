from setuptools import setup, find_packages
# from pathlib import Path
# this_directory = Path(__file__).parent
# long_description = (this_directory / "README.md").read_text()

VERSION = '0.0.2' 
DESCRIPTION = 'Package for scraping data from clubelo.com'
LONG_DESCRIPTION = '''
Package provides functions for obtaining ELO scores for clubs provided by http://clubelo.com/.
As for now, it only enables to get the current ELO of single club
or the clubs featured on the website for the given country or competition.

Data is scraped legally, as http://clubelo.com/robots.txt file allows for it.
'''

setup(
        name="scrapelo", 
        version=VERSION,
        author="Aleks Kapich",
        author_email="aleks.kapich@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['requests', 'bs4', 'pandas'],
        keywords=['python', 'football', 'ELO', 'clubelo', 'scraping', 'data'],
        classifiers= [
            "Development Status :: 2 - Pre-Alpha",
            "Intended Audience :: Other Audience",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)