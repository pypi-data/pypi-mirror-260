import pathlib
from setuptools import setup, find_packages
import os
import codecs

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1' 
DESCRIPTION = 'Mystique : A python package that takes care of obfuscation and encryption of buisness logic.'
LONG_DESCRIPTION = long_description


setup(
        name="Subdora", 
        version=VERSION,
        author="Lakshit Karsoliya",
        author_email="lakshitkumar220@gmail.com",
        description=DESCRIPTION,
        long_description_content_type="text/markdown",

        long_description=LONG_DESCRIPTION,
        url='https://github.com/Lakshit-Karsoliya/Subdora',
        requires=[],

        packages=find_packages(),
        include_package_data=True,
        
        keywords=['python', 'file encryption','security','obfuscation'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3",
            "Operating System :: Unix",
            "Operating System :: Microsoft :: Windows",
        ],
)