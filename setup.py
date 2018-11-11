from setuptools import setup, find_packages
import os
import utt

description = "A simple command-line time tracking application"

long_description = (
    "Ultimate Time Tracker (utt) is a simple command-line time tracking "
    "application. It is intented for people who need to report their time on "
    "another system and want a preliminary time sheet.")

setup(
    author="Mathieu Larose",
    author_email="mathieu@mathieularose.com",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python", "Topic :: Office/Business",
        "Topic :: Utilities"
    ],
    keywords="time tracking",
    license='GPL',
    description=description,
    long_description=long_description,
    name='utt',
    packages=find_packages(),
    url="https://github.com/larose/utt",
    version=utt.__version__,
    install_requires=[
        'argcomplete',
        'python_dateutil',
        'pytz',
        'tzlocal',
    ],
    entry_points={'console_scripts': [
        'utt = utt.__main__:main',
    ]})
