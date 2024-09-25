"""
Developed by Arman Avesta, MD, PhD
FNNDSC | Boston Children's Hospital | Harvard Medical School

This module contains image re-orientation and visualization functions.
"""

# ----------------------------------------------- ENVIRONMENT SETUP ---------------------------------------------------
# Project imports:


# System imports:
import nibabel as nib
import matplotlib.pyplot as plt

# # Print configs:
# np.set_printoptions(precision=1, suppress=True)

# ---------------------------------------------- HELPER FUNCTIONS -----------------------------------------------------

def reorient_nifti(nifti):
    """
    Re-orients NIfTI to LAS+ system = standard radiology system.
    Note that the affine transform of NIfTI file (from the MRI volume space to the scanner space) is also corrected.

    :param nifti: input NIfTI file.
    :return: re-oriented NIfTI in LAS+ system.

    Notes:
    ------
    nib.io_orientation compares the orientation of nifti with RAS+ system. So if nifti is already in
    RAS+ system, the return from nib.io_orientation(nifti.affine) will be:
    [[0, 1],
     [1, 1],
     [2, 1]]
    If nifti is in LAS+ system, the return would be:
    [[0, -1],           # -1 means that the first axis is flipped compared to RAS+ system.
     [1, 1],
     [2, 1]]
    If nifti is in PIL+ system, the return would be:
    [[1, -1],           # P is the 2nd axis in RAS+ hence 1 (not 0), and is also flipped hence -1.
     [2, -1],           # I is the 3rd axis in RAS+ hence 2, and is also flipped hence -1.
     [0, -1]]           # L is the 1st axis in RAS+ hence 0, and is also flipped hence -1.
    Because we want to save images in LAS+ orientation rather than RAS+, in the code below we find axis 0 and
    negate the 2nd column, hence going from RAS+ to LAS+. For instance, for PIL+, the orientation will be:
    [[1, -1],
     [2, -1],
     [0, -1]]
    This is PIL+ compared to RAS+. To compare it to LAS+, we should change it to:
    [[1, -1],
     [2, -1],
     [0, 1]]
    That is what this part of the code does:
    orientation[orientation[:, 0] == 0, 1] = - orientation[orientation[:, 0] == 0, 1]
    Another inefficient way of implementing this function is:
    ################################################################################
    original_orientation = nib.io_orientation(nifti.affine)
    target_orientation = nib.axcodes2ornt(('L', 'A', 'S'))
    orientation_transform = nib.ornt_transform(original_orientation, target_orientation)
    return nifti.as_reoriented(orientation_transform)
    ################################################################################
    """
    orientation = nib.io_orientation(nifti.affine)
    orientation[orientation[:, 0] == 0, 1] = - orientation[orientation[:, 0] == 0, 1]
    return nifti.as_reoriented(orientation)



def imgshow(nifti):
    """
    This function shows a nifti image in LAS+ system.
    """
    kwargs = dict(cmap='gray', origin='lower')
    ndim = nifti.ndim
    assert ndim in (2, 3), f'image shape: {nifti.shape}; imshow can only show 2D and 3D images.'

    if ndim == 2:
        img = nifti.get_fdata()
        plt.imshow(img.T, **kwargs)
        plt.show()

    elif ndim == 3:
        nifti = reorient_nifti(nifti)
        img = nifti.get_fdata()
        voxsize = tuple(float(dim) for dim in nifti.header.get_zooms())

        midaxial = img.shape[2] // 2
        midcoronal = img.shape[1] // 2
        midsagittal = img.shape[0] // 2
        axial_aspect_ratio = voxsize[1] / voxsize[0]
        coronal_aspect_ratio = voxsize[2] / voxsize[0]
        sagittal_aspect_ratio = voxsize[2] / voxsize[1]

        axial = plt.subplot(1, 3, 1)
        plt.imshow(img[:, :, midaxial].T, **kwargs)
        axial.set_aspect(axial_aspect_ratio)
        axial.set_title('axial')

        coronal = plt.subplot(1, 3, 2)
        plt.imshow(img[:, midcoronal, :].T, **kwargs)
        coronal.set_aspect(coronal_aspect_ratio)
        coronal.set_title('coronal')

        sagittal = plt.subplot(1, 3, 3)
        plt.imshow(img[midsagittal, :, :].T, **kwargs)
        sagittal.set_aspect(sagittal_aspect_ratio)
        sagittal.set_title('sagittal')

        plt.show()



# -------------------------------------------------- CODE TESTING -----------------------------------------------------

if __name__ == '__main__':
    nifti = nib.load('/Users/arman/projects/pl-image-register/data/nifti/fixed.nii.gz')
    imgshow(nifti)