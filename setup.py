"""
--------------------------
DownStream Setup.py Script
--------------------------

"""
from setuptools import setup

setup(
    name="downstream",
    version='0.1.0',
    url='https://github.com/swc2124/tweetspy.git',
    author='sol courtney',
    author_email='sol.courtney@gmail.com',
    packages=[],
    install_requires=[
        "tweepy>=3.6",
        "country_list>0.1",
        "colorama>=0.3.0",
        "langdetect>=1.0",
        "nltk>=3.3",
        "pymongo>=3.4",
        "psutil>=5.0"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
