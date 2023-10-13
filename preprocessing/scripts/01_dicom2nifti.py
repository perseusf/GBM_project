import os
import argparse
from pathlib import Path
from burdenko_glioma.nifti import dicom_to_nifti


def main(root, target_folder):
    for patient_folder in sorted(os.listdir(root)):
        # Define the save path for NIfTI files for the current patient
        save_path = os.path.join(target_folder, patient_folder, 'image')
        
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        
        # Iterate through subfolders within the patient folder
        for subfolder in os.listdir(Path(root) / patient_folder):
            # Identify the baseline visit folder for radiotherapy planning
            if 'Radiotherapy planning' in subfolder:
                baseline_visit = subfolder
        
        source_folder = Path(root) / patient_folder / baseline_visit
        rt_folders = ['RTSTRUCT', 'RTPLAN', 'RTDOSE']
        
        for subfolder in source_folder.glob('*'):
            if not any([stop in subfolder.name for stop in rt_folders]):
                dicom_to_nifti(subfolder, save_path, name=subfolder.name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process DICOM files and convert to NIfTI format.")
    parser.add_argument("-i", "--input", required=True, help="Input root folder")
    parser.add_argument("-o", "--output", required=True, help="Output target folder")
    args = parser.parse_args()

    main(args.input, args.output)