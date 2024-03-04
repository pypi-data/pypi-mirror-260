#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import MathematicalMethodsForRoboticsVisionAndGraphicsLectureNotesStanfordCs205
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('MathematicalMethodsForRoboticsVisionAndGraphicsLectureNotesStanfordCs205'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="mathematical-methods-for-robotics-vision-and-graphics-lecture-notes-stanford-cs205",
    version=MathematicalMethodsForRoboticsVisionAndGraphicsLectureNotesStanfordCs205.__version__,
    url="https://github.com/apachecn/mathematical-methods-for-robotics-vision-and-graphics-lecture-notes-stanford-cs205",
    author=MathematicalMethodsForRoboticsVisionAndGraphicsLectureNotesStanfordCs205.__author__,
    author_email=MathematicalMethodsForRoboticsVisionAndGraphicsLectureNotesStanfordCs205.__email__,
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
    description="Mathematical Methods for Robotics, Vision, and Graphics Lecture Notes (Stanford CS205)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "mathematical-methods-for-robotics-vision-and-graphics-lecture-notes-stanford-cs205=MathematicalMethodsForRoboticsVisionAndGraphicsLectureNotesStanfordCs205.__main__:main",
            "MathematicalMethodsForRoboticsVisionAndGraphicsLectureNotesStanfordCs205=MathematicalMethodsForRoboticsVisionAndGraphicsLectureNotesStanfordCs205.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
