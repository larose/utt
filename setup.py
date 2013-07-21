#!/usr/bin/env python3

from   distutils.core import setup
import os

description = "A simple command-line time tracking application"

long_description="Ultimate Time Tracking (utt) is a simple " \
    "command-line time tracking application. It's designed " \
    "for users that need to report their time on another system and " \
    "want a preliminary timesheet."

setup(
    author="Mathieu Larose",
    author_email="mathieu@mathieularose.com",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Topic :: Office/Business"
        ],
    keywords="time tracking",
    license='GPL',
    description=description,
    long_description=long_description,
    name='utt',
    packages=['utt', 'utt.cmd_report'],
    scripts=[os.path.join('bin', 'utt')],
    url="https://github.com/larose/utt",
    version='1.0',
    )
