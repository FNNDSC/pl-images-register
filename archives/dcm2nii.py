import os
import subprocess


def convert_dicom_to_nifti(dicom_folder, output_folder):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Command to run dcm2niix
    command = [
        'dcm2niix',  # dcm2niix executable
        '-z', 'y',  # Enable compression
        '-o', output_folder,  # Output folder
        dicom_folder  # Input DICOM folder
    ]

    # Run the command
    subprocess.run(command, check=True)
    print(f"Conversion complete. NIfTI files are saved in {output_folder}")



if __name__ == '__main__':
    # Define paths
    dicom_folder = '/Users/arman/projects/pl-image-register/data/ALD_dicom'  # Path to folder containing DICOMs
    output_folder = '/Users/arman/projects/pl-image-register/data/nifti'  # Path to folder to save NIfTI file

    # Convert DICOM to NIfTI
    convert_dicom_to_nifti(dicom_folder, output_folder)

