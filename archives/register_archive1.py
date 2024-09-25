
from nipype.interfaces.fsl import FLIRT         # This requires FSL to be installed on the computer for it to work



def register_images_rigid(fixed_image_path, moving_image_path, registered_moving_image_path, transform_matrix_path,
                          dof=6, cost='mutualinfo'):

    flirt = FLIRT()                             # https://fsl.fmrib.ox.ac.uk/fsl/docs/#/registration/flirt/index
    flirt.inputs.reference = fixed_image_path
    flirt.inputs.in_file = moving_image_path
    flirt.inputs.out_file = registered_moving_image_path
    flirt.inputs.out_matrix_file = transform_matrix_path
    flirt.inputs.dof = dof      # Degrees of freedom should be 6 for rigid registration
    flirt.inputs.cost = cost    # mutual information or normalized mutual information are best options

    result = flirt.run()
    print(f' >>>>> results: {result}')
    print(f"Registered image saved to {registered_moving_image_path}")
    print(f"Transform matrix saved to {transform_matrix_path}")




# CODE TESTING:

if __name__ == '__main__':
    fixed_image_path = '/Users/arman/projects/register_image/data/nifti/fixed.nii.gz'
    moving_image_path = '/Users/arman/projects/register_image/data/nifti/moving.nii.gz'
    registered_moving_image_path = '/Users/arman/projects/register_image/data/nifti/moving_registered.nii.gz'
    transform_matrix_path = '/Users/arman/projects/register_image/data/nifti/transform.mat'

    register_images_rigid(fixed_image_path, moving_image_path, registered_moving_image_path, transform_matrix_path)

    #  1. FLIRT takes ~2 minutes to complete. Will explore faster rigid registration strategies. It would be
    #  great if we can figure out what registration strategy Visage uses, because that takes ~10 seconds.
    #  2. the registered image is a bit blurrier than the original image. Will explore better resampling strategies
    #  such as B-spline interpolation.