#!/usr/bin/env python
"""
Developed by Arman Avesta, MD, PhD
FNNDSC | Boston Children's Hospital | Harvard Medical School

This module contains argument parsing and main function for the image_register plugin.
"""
# --------------------------------------------- ENVIRONMENT SETUP -----------------------------------------------------
# Project imports:
from registration_tools import rigid_registration

# System imports:
from os.path import join
from pathlib import Path
from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
from chris_plugin import chris_plugin

# Version:
__version__ = '1.0.1'

# ---------------------------------------------- ARGUMENT PARSING -----------------------------------------------------

DISPLAY_TITLE = r"""
       _        _                                                       _     _            
      | |      (_)                                                     (_)   | |           
 _ __ | |______ _ _ __ ___   __ _  __ _  ___  ___ ______ _ __ ___  __ _ _ ___| |_ ___ _ __ 
| '_ \| |______| | '_ ` _ \ / _` |/ _` |/ _ \/ __|______| '__/ _ \/ _` | / __| __/ _ \ '__|
| |_) | |      | | | | | | | (_| | (_| |  __/\__ \      | | |  __/ (_| | \__ \ ||  __/ |   
| .__/|_|      |_|_| |_| |_|\__,_|\__, |\___||___/      |_|  \___|\__, |_|___/\__\___|_|   
| |                                __/ |                           __/ |                   
|_|                               |___/                           |___/                    
"""

parser = ArgumentParser(description='This plugin registers a moving 3D image (CT, MRI, PET, etc) onto another'
                                    'fixed image and saves the registered moving image as well as '
                                    'the transformation matrix. The fixed, moving, and registered moving images '
                                    'are all in NIfTI format.',
                        formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('-V', '--version', action='version',
                    version=f'%(prog)s {__version__}')

parser.add_argument('--fixed_image', type=str, default='fixed_image.nii.gz',
                    help='relative path to the fixed image in relation to input folder')
parser.add_argument('--moving_image', type=str, default='moving_image.nii.gz',
                    help='relative path to the moving image in relation to input folder')
parser.add_argument('--registered_image', type=str, default='registered_image.nii.gz',
                    help='relative path to the registered image in relation to output folder')
parser.add_argument('--transform_matrix', type=str, default='transform.mat',
                    help='relative path to the transformation matrix in relation to output folder')

# The main function of this *ChRIS* plugin is denoted by this ``@chris_plugin`` "decorator."
# Some metadata about the plugin is specified here. There is more metadata specified in setup.py.
#
# documentation: https://fnndsc.github.io/chris_plugin/chris_plugin.html#chris_plugin

# ------------------------------------------- ChRIS PLUGIN WRAPPER ----------------------------------------------------
@chris_plugin(
    parser=parser,
    title='Images registration',
    category='3D image processing',     # ref. https://chrisstore.com/plugins
    min_memory_limit='1Gi',             # supported units: Mi, Gi
    min_cpu_limit='1000m',              # millicores, e.g. "1000m" = 1 CPU core
    min_gpu_limit=0                     # set min_gpu_limit=1 to enable GPU
)
# ----------------------------------------------- MAIN FUNCTION -------------------------------------------------------

def main(options: Namespace, inputdir: Path, outputdir: Path):
    """
    *ChRIS* plugins usually have two positional arguments: an **input directory** containing
    input files and an **output directory** where to write output files. Command-line arguments
    are passed to this main method implicitly when ``main()`` is called below without parameters.

    :param options: non-positional arguments parsed by the parser given to @chris_plugin
    :param inputdir: directory containing (read-only) input files
    :param outputdir: directory where to write output files
    """
    print(DISPLAY_TITLE)

    fixed_image_path = join(inputdir, options.fixed_image)
    moving_image_path = join(inputdir, options.moving_image)
    registered_image_path = join(outputdir, options.registered_image)
    transform_matrix_path = join(outputdir, options.transform_matrix)

    rigid_registration(fixed_image_path, moving_image_path, registered_image_path, transform_matrix_path)

# ------------------------------------------------ EXECUTE MAIN -------------------------------------------------------

if __name__ == '__main__':
    main()
