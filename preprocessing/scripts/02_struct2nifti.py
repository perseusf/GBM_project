import os
import numpy as np
import argparse
from pathlib import Path
from burdenko_glioma.nifti import dicom_to_nifti
from dcmrtstruct2nii import dcmrtstruct2nii


def main(root, target_folder):
    for patient_folder in sorted(os.listdir(root)):
        save_path = os.path.join(target_folder, patient_folder, 'rt')
        
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        
        for subfolder in os.listdir(Path(root) / patient_folder):
            # Identify the baseline visit folder for radiotherapy planning
            if 'Radiotherapy planning' in subfolder:
                baseline_visit = subfolder
                
                # Find the CT scan associated with the radiotherapy planning
                for fname in os.listdir(Path(root) / patient_folder / subfolder):
                    if "CT00CT" in fname:
                        ct_path = Path(root) / patient_folder / subfolder / fname
        
        source_folder = Path(root) / patient_folder / baseline_visit
        
        rt_folders = ['RTSTRUCT']
        
        for subfolder in source_folder.glob('*'):
            if any([stop in subfolder.name for stop in rt_folders]):
                dcmrtstruct2nii(subfolder / '1-1.dcm', ct_path, save_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process RT files and convert to NIfTI format.")
    parser.add_argument("-i", "--input", required=True, help="Input root folder")
    parser.add_argument("-o", "--output", required=True, help="Output target folder")
    args = parser.parse_args()

    main(args.input, args.output)
