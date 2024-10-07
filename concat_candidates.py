import os
import glob
import paths
from tqdm import tqdm

# Define the input directory and output file
input_dir = paths.CANDIDATES_FOLDER_PATH
output_file = paths.CANDIDATES_FILE_PATH

# Open the output file in write mode
with open(output_file, 'w') as outfile:
    # Loop through each JSON file in the input directory
    first=True
    #for json_file in tqdm(glob.glob(os.path.join(input_dir, '*.json'))):
    for json_file in input_dir.iterdir():
        # Open and read the content of the JSON file
        with open(json_file, 'r') as infile:
            if not first:
                outfile.write('\n')
            outfile.write(infile.read().strip())
            first=False

print(f"All JSON files have been concatenated into {output_file}")