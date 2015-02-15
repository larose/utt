from distutils.core import setup
import os

description = "A simple command-line time tracking application"

long_description = (
    "Ultimate Time Tracker (utt) is a simple command-line time tracking "
    "application. It is intented for people who need to report their time on "
    "another system and want a preliminary time sheet."
)

setup(
    author="Mathieu Larose",
    author_email="mathieu@mathieularose.com",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
        "Topic :: Office/Business",
        "Topic :: Utilities"
    ],
    keywords="time tracking",
    license='GPL',
    description=description,
    long_description=long_description,
    name='utt',
    packages=['utt'],
    scripts=[os.path.join('bin', 'utt')],
    url="https://github.com/larose/utt",
    version=open('VERSION').readline(),
)
