import os
from setuptools import setup, find_packages

# FUNCTION TO READ THE README FILE
def read_file(filename):
    with open(
        os.path.join(os.path.dirname(__file__), filename), encoding="utf-8"
    ) as file:
        return file.read()

setup(
    name="MediaSwift",
    version="2.3.1",
    author="ROHIT SINGH",
    author_email="rs3232263@gmail.com",
    description="A MediaSwift PYTHON PACKAGE FOR MEDIA CONVERSION PLAY AND PROBING.",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/ROHIT-SINGH-1/PYTHON-MEDIASWIFT.git",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Video",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="MEDIA VIDEO CONVERSION PROBING AND PLAYING.",
    python_requires=">=3.8",
    license="GPL-3.0",
    project_urls={
        "Documentation": "https://github.com/ROHIT-SINGH-1/PYTHON-MEDIASWIFT/blob/main/README.md",
        "Source Code": "https://github.com/ROHIT-SINGH-1/PYTHON-MEDIASWIFT",
        "Bug Tracker": "https://github.com/ROHIT-SINGH-1/PYTHON-MEDIASWIFT/issues",
    },
    install_requires=[
        "rich",
        "tqdm",
        "numpy",
    ],
    entry_points={
        "console_scripts": [
            "ffpe = MediaSwift.ffpe:ffpe",
            "ffpr = MediaSwift.ffpr:ffpr",
            "ffpl = MediaSwift.ffpl:ffpl",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
