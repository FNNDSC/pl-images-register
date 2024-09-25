
import subprocess
from datetime import datetime
import SimpleITK as sitk
import numpy as np
import nibabel as nib

from visualization_tools import imgshow


def register_images_rigid(fixed_image_path, moving_image_path, registered_moving_image_path, transform_matrix_path,
                          dof='6', cost='mutualinfo'):
    """
    This function needs FSL's FLIRT to be able to run: https://fsl.fmrib.ox.ac.uk/fsl/docs/#/registration/flirt/index
    """
    flirt_command = [
        'flirt',
        '-ref', fixed_image_path,
        '-in', moving_image_path,
        '-out', registered_moving_image_path,
        '-omat', transform_matrix_path,
        '-dof', dof,  # Degrees of freedom should be '6' for rigid body transformation
        '-cost', cost  # multual information or normalized mutual information are best options
    ]
    subprocess.run(flirt_command, check=True)
    print(f"Registered image saved to {registered_moving_image_path}")
    print(f"Transform matrix saved to {transform_matrix_path}")


def resample_image(fixed_image_path, moving_image_path, registered_moving_image_path, transform_matrix_path):
    """
    Resample a moving 3D image using a transform matrix to match the space of a fixed 3D image.

    Parameters:
    moving_image_path (str): Path to the moving image file (e.g., 'moving.nii.gz').
    fixed_image_path (str): Path to the fixed image file (e.g., 'fixed.nii.gz').
    transform_matrix_path (str): Path to the transform matrix file (e.g., 'transform.mat').
    registered_image_path (str): Path to save the resampled moving image (e.g., 'moving_registered.nii.gz').

    Returns:
    None
    """
    # Read the transform matrix from the file
    transform_matrix = np.loadtxt(transform_matrix_path)
    # print(f'transform_matrix: {transform_matrix}')

    # Create an affine transform
    transform = sitk.AffineTransform(3)
    transform.SetMatrix(transform_matrix[:3, :3].flatten())
    transform.SetTranslation(transform_matrix[:3, 3])

    # Load the moving and fixed images
    fixed_image = sitk.ReadImage(fixed_image_path, sitk.sitkFloat32)
    moving_image = sitk.ReadImage(moving_image_path, sitk.sitkFloat32)

    # Resample the moving image
    resampler = sitk.ResampleImageFilter()
    resampler.SetReferenceImage(fixed_image)
    resampler.SetTransform(transform)
    resampler.SetInterpolator(sitk.sitkLinear)

    # Apply the transformation
    moving_resampled = resampler.Execute(moving_image)

    # Save the resampled moving image
    sitk.WriteImage(moving_resampled, registered_moving_image_path)

    print(f"Resampling completed and saved as '{registered_moving_image_path}'")

# Example usage:
# resample_image('moving.nii.gz', 'fixed.nii.gz', 'transform.mat', 'moving_registered.nii.gz')




# CODE TESTING:

if __name__ == '__main__':
    fixed_image_path = '/Users/arman/projects/register_image/data/nifti/fixed.nii.gz'
    moving_image_path = '/Users/arman/projects/register_image/data/nifti/moving.nii.gz'
    registered_moving_image_path = '/Users/arman/projects/register_image/data/nifti/moving_registered.nii.gz'
    transform_matrix_path = '/Users/arman/projects/register_image/data/nifti/transform.mat'

    t1 = datetime.now()
    register_images_rigid(fixed_image_path, moving_image_path, registered_moving_image_path, transform_matrix_path)
    print(f'Registration computation time: {datetime.now() - t1}')

    nifti = nib.load(registered_moving_image_path)
    imgshow(nifti)

    # Test results show that:
    #  1. FLIRT takes ~2 minutes to complete. Will explore faster rigid registration strategies. It would be
    #  great if we can figure out what registration strategy Visage uses, because that takes ~10 seconds.
    #  2. the registered image is a bit blurrier than the original image. Will explore better resampling strategies
    #  such as B-spline interpolation.
