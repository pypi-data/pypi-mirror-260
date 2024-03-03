#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import AlgorithmicInformationTheoryReviewForPhysicistsAndNaturalScientists
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('AlgorithmicInformationTheoryReviewForPhysicistsAndNaturalScientists'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="algorithmic-information-theory-review-for-physicists-and-natural-scientists",
    version=AlgorithmicInformationTheoryReviewForPhysicistsAndNaturalScientists.__version__,
    url="https://github.com/apachecn/algorithmic-information-theory-review-for-physicists-and-natural-scientists",
    author=AlgorithmicInformationTheoryReviewForPhysicistsAndNaturalScientists.__author__,
    author_email=AlgorithmicInformationTheoryReviewForPhysicistsAndNaturalScientists.__email__,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: Other/Proprietary License",
        "Natural Language :: Chinese (Simplified)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Text Processing :: Markup :: Markdown",
        "Topic :: Text Processing :: Markup :: HTML",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Documentation",
        "Topic :: Documentation",
    ],
    description="Algorithmic Information Theory - Review For Physicists And Natural Scientists",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "algorithmic-information-theory-review-for-physicists-and-natural-scientists=AlgorithmicInformationTheoryReviewForPhysicistsAndNaturalScientists.__main__:main",
            "AlgorithmicInformationTheoryReviewForPhysicistsAndNaturalScientists=AlgorithmicInformationTheoryReviewForPhysicistsAndNaturalScientists.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
