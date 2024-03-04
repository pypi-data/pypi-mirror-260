from setuptools import setup, find_packages
from pathlib import Path


VERSION = '0.0.4' 
DESCRIPTION = 'Package for scraping data from clubelo.com'
LONG_DESCRIPTION = (Path(__file__).parent / "README.md").read_text()

setup(
        name="scrapelo", 
        version=VERSION,
        author="Aleks Kapich",
        author_email="aleks.kapich@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type='text/markdown',
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