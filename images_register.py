#!/usr/bin/env python
"""
Developed by Arman Avesta, MD, PhD
FNNDSC | Boston Children's Hospital | Harvard Medical School

This module contains argument parsing and main function for the image_register plugin.
"""
# --------------------------------------------- ENVIRONMENT SETUP -----------------------------------------------------
# Project imports:
from registration_tools import rigid_registration
from os_tools import sub_niftis

# System imports:
from os.path import join
from pathlib import Path
from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
from chris_plugin import chris_plugin

# Version:
# __version__ = '1.0.1'

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

# parser.add_argument('-V', '--version', action='version',
#                     version=f'%(prog)s {__version__}')

"""
If there is only one moving image, it will be registered onto the fixed image.
If there are multiple moving images, each one will be registered to the fixed image separately.

For multiple moving images, all of them should be placed in a folder, and the folder should be passed to the 
parser under moving_images_folder.

Example 1:
 
Inputs: 
    input_dir/fixed_image.nii.gz
    input_dir/moving_image.nii.gz 

Outputs:
    output_dir/moving_image_registered.nii.gz
    output_dir/moving_image_transform.mat

Example 2:

Inputs: 
    input_dir/fixed_image.nii.gz
    input_dir/moving_images_folder/moving_image1.nii.gz, moving_image2.nii.gz, moving_image3.nii.gz, etc.

Outputs:
    output_dir/moving_images_folder/moving_image1_registered.nii.gz, moving_image2_registered.nii.gz, 
        moving_image3.nii.gz, etc.
    output_dir/moving_images_folder/moving_image1_transform.mat, moving_image2_transform.mat, 
        moving_image3_transform.mat, etc.
        
Please not that all images (fixed, moving, registered) must be in nii.gz format.
"""

parser.add_argument('--fixed_image', type=str, default='fixed_image.nii.gz',
                    help='relative path to the fixed image in relation to input folder')
parser.add_argument('--moving_image', type=str, default='moving_image.nii.gz',
                    help='relative path to the moving image in relation to input folder.'
                         'The moving image must be in .nii.gz format.')
parser.add_argument('--moving_images_folder', type=str, default='None',
                    help='relative path to the folder containing multiple moving images.'
                         'Every image in this folder will be registered to the fixed image.'
                         'All moving images must be in .nii.gz format.')

# ------------------------------------------- ChRIS PLUGIN WRAPPER ----------------------------------------------------

# The main function of this *ChRIS* plugin is denoted by this ``@chris_plugin`` "decorator."
# Some metadata about the plugin is specified here. There is more metadata specified in setup.py.
#
# documentation: https://fnndsc.github.io/chris_plugin/chris_plugin.html#chris_plugin

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

    if options.moving_images_folder == 'None':
        moving_image_path = join(inputdir, options.moving_image)
        registered_image_path = join(outputdir, options.moving_image.replace('.nii.gz', '_registered.nii.gz'))
        transform_matrix_path = join(outputdir, options.moving_image.replace('.nii.gz', '_transform.mat'))

        rigid_registration(fixed_image_path, moving_image_path, registered_image_path, transform_matrix_path)

    else:
        moving_images_list = sub_niftis(join(inputdir, options.moving_images_folder), complete_path=False)
        for moving_image in moving_images_list:
            moving_image_path = join(inputdir, options.moving_images_folder, moving_image)
            registered_image_path = join(outputdir, options.moving_images_folder,
                                         options.moving_image.replace('.nii.gz', '_registered.nii.gz'))
            transform_matrix_path = join(outputdir, options.moving_images_folder,
                                          options.moving_image.replace('.nii.gz', '_transform.mat'))
            rigid_registration(fixed_image_path, moving_image_path, registered_image_path, transform_matrix_path)

# ------------------------------------------------ EXECUTE MAIN -------------------------------------------------------

if __name__ == '__main__':
    main()
