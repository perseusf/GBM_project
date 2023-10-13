import os
from ants.utils.convert_nibabel import to_nibabel
from burdenko_glioma.registration import rigid_reg
import argparse
import nibabel as nib


def main(root, target_folder):

    for patient_folder in sorted(os.listdir(root)):
        save_path = os.path.join(target_folder, patient_folder, 'warped')

        if not os.path.exists(save_path):
            os.makedirs(save_path)

        for subfolder in os.listdir(os.path.join(root, patient_folder)):
            if 'image' in subfolder:
                baseline_visit = subfolder
                for fname in os.listdir(os.path.join(root, patient_folder, subfolder)):
                    if ("CT00CT" in fname) and ('.nii' in fname):
                        fixed_image_path = os.path.join(root, patient_folder, subfolder, fname)
                    if ("MR00T1" in fname) and ('.nii' in fname):
                        moving_imageMR00T1_path = os.path.join(root, patient_folder, subfolder, fname)
                    if ("MR00T2" in fname) and ('.nii' in fname):
                        moving_imageMR00T2_path = os.path.join(root, patient_folder, subfolder, fname)
                    if ("MRCET1" in fname) and ('.nii' in fname):
                        moving_imageMRCET1_path = os.path.join(root, patient_folder, subfolder, fname)
                    if ("MR0T2FLAIR" in fname) and ('.nii' in fname):
                        moving_imageMR0T2FLAIR_path = os.path.join(root, patient_folder, subfolder, fname)

        if moving_imageMR00T1_path is not None:
            warped_MR00T1 = rigid_reg(fixed_image_path, moving_imageMR00T1_path, None)
            nib.save(to_nibabel(warped_MR00T1), os.path.join(save_path, 'warped_MR00T1'))
        if moving_imageMR00T2_path is not None:
            warped_MR00T2 = rigid_reg(fixed_image_path, moving_imageMR00T2_path, None)
            nib.save(to_nibabel(warped_MR00T2), os.path.join(save_path, 'warped_MR00T2'))
        if moving_imageMRCET1_path is not None:
            warped_MRCET1 = rigid_reg(fixed_image_path, moving_imageMRCET1_path, None)
            nib.save(to_nibabel(warped_MRCET1), os.path.join(save_path, 'warped_MRCET1'))
        if moving_imageMR0T2FLAIR_path is not None:
            warped_MR0T2FLAIR = rigid_reg(fixed_image_path, moving_imageMR0T2FLAIR_path, None)
            nib.save(to_nibabel(warped_MR0T2FLAIR), os.path.join(save_path, 'warped_MR0T2FLAIR'))

        print(f'Finished warping {fixed_image_path}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process RT files and convert to NIfTI format.")
    parser.add_argument("-i", "--input", required=True, help="Input root folder")
    parser.add_argument("-o", "--output", required=True, help="Output target folder")
    args = parser.parse_args()

    main(args.input, args.output)
