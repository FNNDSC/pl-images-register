"""
Developed by Arman Avesta, MD, PhD
FNNDSC | Boston Children's Hospital | Harvard Medical School

This module sets up the image registration plugin.
"""

# ----------------------------------------------- ENVIRONMENT SETUP ---------------------------------------------------
# Global variables:
VERSION='1.0.0'     # <-------------------------- SET VERSION HERE

# Project imports:


# System imports:
from setuptools import setup
import re

# ------------------------------------------------ HELPER FUNCTIONS ---------------------------------------------------

def parse_requirements(file_path):
    """
    Parse the requirements.txt file and return a list of requirements, ignoring comments.

    Parameters:
    file_path (str): Path to the requirements.txt file.

    Returns:
    list: List of package names.
    """
    requirements = []
    with open(file_path, 'r') as file:
        for line in file:
            # Strip whitespace and newline characters
            line = line.strip()
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            # Split the line on the first occurrence of '~='
            package = line.split('~=')[0]
            requirements.append(package)

    return requirements

# def get_version(rel_path: str) -> str:
#     """
#     Searches for the ``__version__ = `` line in a source code file.
#
#     https://packaging.python.org/en/latest/guides/single-sourcing-package-version/
#     """
#     _version_re = re.compile(r"(?<=^__version__ = (\"|'))(.+)(?=\"|')")
#     with open(rel_path, 'r') as f:
#         matches = map(_version_re.search, f)
#         filtered = filter(lambda m: m is not None, matches)
#         version = next(filtered, None)
#         if version is None:
#             raise RuntimeError(f'Could not find __version__ in {rel_path}')
#         return version.group(0)


# ------------------------------------------------- MAIN FUNCTIONS ----------------------------------------------------

setup(
    name='images-register',
    # version=get_version('images_register.py'),
    version=VERSION,
    description='A ChRIS plugin to do multiple image registration',
    author='FNNDSC',
    author_email='arman.avasta@childrens.harvard.edu',
    url='https://github.com/FNNDSC/pl-images-register',
    py_modules=['images_register'],
    install_requires=['chris_plugin'],
    license='MIT',
    entry_points={
        'console_scripts': [
            'images_register = images_register:main'
        ]
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Medical Science Apps.'
    ],
    extras_require={
        'none': [],
        'dev': [
            'pytest~=7.1'
        ]
    }
)


# -------------------------------------------------- CODE TESTING -----------------------------------------------------

