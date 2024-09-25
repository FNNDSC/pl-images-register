"""
Developed by Arman Avesta, MD, PhD
FNNDSC | Boston Children's Hospital | Harvard Medical School

This file contains functions to help with file & folder organization, parallel processing, and other operating system
functionalities.
"""

# ----------------------------------------------- ENVIRONMENT SETUP ---------------------------------------------------
# Project imports:

# System imports:
import os
from os.path import join, dirname
from typing import List

# ---------------------------------------------- HELPER FUNCTIONS -----------------------------------------------------

def subdirs(root: str, complete_path: bool = False, prefix: str = None, suffix: str = None, sort: bool = True) \
        -> List[str]:
    if complete_path:
        func = os.path.join
    else:
        func = lambda x, y: y
    res = [func(root, subdir) for subdir in os.listdir(root) if os.path.isdir(join(root, subdir))
           and (prefix is None or subdir.startswith(prefix))
           and (suffix is None or subdir.endswith(suffix))]
    if sort:
        res.sort()
    return res


def subfiles(root: str, complete_path: bool = True, prefix: str = None, suffix: str = None, sort: bool = True) \
        -> List[str]:
    if complete_path:
        func = os.path.join
    else:
        func = lambda x, y: y
    res = [func(root, subdir) for subdir in os.listdir(root) if os.path.isfile(join(root, subdir))
           and (prefix is None or subdir.startswith(prefix))
           and (suffix is None or subdir.endswith(suffix))]
    if sort:
        res.sort()
    return res


def sub_niftis(root: str, complete_path: bool = True, sort: bool = True) -> List[str]:
    return subfiles(root, complete_path=complete_path, sort=sort, suffix='.nii.gz')



def split_path(path: str) -> List[str]:
    """
    splits at each separator. This is different from os.path.split which only splits at last separator
    """
    return path.split(os.sep)


# -------------------------------------------------- CODE TESTING -----------------------------------------------------

if __name__ == '__main__':

    path = '/Users/arman/projects/pl-images-register/data/nifti'
    niftis_list = sub_niftis(path, complete_path=False)
    print(niftis_list)