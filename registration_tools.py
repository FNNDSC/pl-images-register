"""
Developed by Arman Avesta, MD, PhD
FNNDSC | Boston Children's Hospital | Harvard Medical School

This module contains image registration functions.
"""

# ----------------------------------------------- ENVIRONMENT SETUP ---------------------------------------------------
# Project imports:
from visualization_tools import imgshow

# System imports:
import SimpleITK as sitk
import nibabel as nib
import os
from datetime import datetime

# ---------------------------------------------- HELPER FUNCTIONS -----------------------------------------------------


# ----------------------------------------------- MAIN FUNCTIONS ------------------------------------------------------

def rigid_registration(fixed_image_path, moving_image_path, registered_image_path, transform_matrix_path):
    # Read the images
    fixed_image = sitk.ReadImage(fixed_image_path, sitk.sitkFloat32)
    moving_image = sitk.ReadImage(moving_image_path, sitk.sitkFloat32)

    # Initialize the transform
    initial_transform = sitk.CenteredTransformInitializer(fixed_image,
                                                          moving_image,
                                                          sitk.Euler3DTransform(),
                                                          sitk.CenteredTransformInitializerFilter.GEOMETRY)

    # Set up the multi-resolution framework
    registration_method = sitk.ImageRegistrationMethod()
    registration_method.SetShrinkFactorsPerLevel(shrinkFactors=[4, 2, 1])
    registration_method.SetSmoothingSigmasPerLevel(smoothingSigmas=[2, 1, 0])
    registration_method.SmoothingSigmasAreSpecifiedInPhysicalUnitsOn()

    # Set up the registration components
    registration_method.SetMetricAsMattesMutualInformation(numberOfHistogramBins=50)
    registration_method.SetMetricSamplingStrategy(registration_method.RANDOM)
    registration_method.SetMetricSamplingPercentage(0.01)
    registration_method.SetInterpolator(sitk.sitkLinear)

    registration_method.SetOptimizerAsGradientDescent(learningRate=1.0, numberOfIterations=100,
                                                      convergenceMinimumValue=1e-6, convergenceWindowSize=10)
    registration_method.SetOptimizerScalesFromPhysicalShift()

    registration_method.SetInitialTransform(initial_transform, inPlace=False)
    registration_method.SetOptimizerScalesFromJacobian()

    # Execute the registration
    final_transform = registration_method.Execute(fixed_image, moving_image)

    # print(f"Final metric value: {registration_method.GetMetricValue()}")
    # print(f"Optimizer's stopping condition: {registration_method.GetOptimizerStopConditionDescription()}")

    # Apply the transform to the moving image
    resampled_moving_image = sitk.Resample(moving_image, fixed_image, final_transform, sitk.sitkBSpline, 0.0,
                                           moving_image.GetPixelID())

    # Save the registered image
    if os.path.exists(registered_image_path):
        os.remove(registered_image_path)
    sitk.WriteImage(resampled_moving_image, registered_image_path)

    # Save the transform matrix
    if os.path.exists(transform_matrix_path):
        os.remove(transform_matrix_path)
    sitk.WriteTransform(final_transform, transform_matrix_path)


# -------------------------------------------------- CODE TESTING -----------------------------------------------------

if __name__ == '__main__':
    fixed_image_path = '/Users/arman/projects/pl-images-register/data/nifti/fixed.nii.gz'
    moving_image_path = '/Users/arman/projects/pl-images-register/data/nifti/moving.nii.gz'
    registered_image_path = '/Users/arman/projects/pl-images-register/data/nifti/moving_registered.nii.gz'
    transform_matrix_path = '/Users/arman/projects/pl-images-register/data/nifti/transform.mat'

    t1 = datetime.now()
    rigid_registration(fixed_image_path, moving_image_path, registered_image_path, transform_matrix_path)
    print(f'Registration computation time: {datetime.now() - t1}')

    fixed_image = nib.load(fixed_image_path)
    moving_image = nib.load(moving_image_path)
    registered_image = nib.load(registered_image_path)
    imgshow(fixed_image)
    imgshow(moving_image)
    imgshow(registered_image)

