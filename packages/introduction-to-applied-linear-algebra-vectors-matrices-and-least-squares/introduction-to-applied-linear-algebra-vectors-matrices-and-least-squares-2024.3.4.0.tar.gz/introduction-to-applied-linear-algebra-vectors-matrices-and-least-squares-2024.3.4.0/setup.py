#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import IntroductionToAppliedLinearAlgebraVectorsMatricesAndLeastSquares
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('IntroductionToAppliedLinearAlgebraVectorsMatricesAndLeastSquares'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="introduction-to-applied-linear-algebra-vectors-matrices-and-least-squares",
    version=IntroductionToAppliedLinearAlgebraVectorsMatricesAndLeastSquares.__version__,
    url="https://github.com/apachecn/introduction-to-applied-linear-algebra-vectors-matrices-and-least-squares",
    author=IntroductionToAppliedLinearAlgebraVectorsMatricesAndLeastSquares.__author__,
    author_email=IntroductionToAppliedLinearAlgebraVectorsMatricesAndLeastSquares.__email__,
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
    description="Introduction to Applied Linear Algebra – Vectors, Matrices, and Least Squares",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "introduction-to-applied-linear-algebra-vectors-matrices-and-least-squares=IntroductionToAppliedLinearAlgebraVectorsMatricesAndLeastSquares.__main__:main",
            "IntroductionToAppliedLinearAlgebraVectorsMatricesAndLeastSquares=IntroductionToAppliedLinearAlgebraVectorsMatricesAndLeastSquares.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
