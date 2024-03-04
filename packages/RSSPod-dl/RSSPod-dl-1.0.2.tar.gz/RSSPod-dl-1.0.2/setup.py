from setuptools import find_packages, setup
import os

VERSION = '1.0.2'
DESCRIPTION = 'Python CLI tool for downloading and managing podcast from RSS feeds.'

# Read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="RSSPod-dl",
    version=VERSION,
    packages=find_packages(),
    install_requires=['bs4', 'eyed3', 'alive_progress', "lxml"],
    entry_points={
        'console_scripts': [
            'rsspod=RSSPod_dl.main:main',
        ],
    },

    author="mariout",
    url='https://github.com/rimaout/RSSPod-dl',  
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT', 
    keywords=['python', 'podcast downloader', 'RSS'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
    ]
)
