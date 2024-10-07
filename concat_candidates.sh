#!/bin/bash

# Define the input directory and output file
input_dir="output_files/el_candidates"
output_file="output_files/el_candidates.jsonl"

# Create or clear the output file
> "$output_file"

# Loop through each JSON file in the input directory
for json_file in "$input_dir"/*.json; do
  # Append the content of the JSON file to the output file
  cat "$json_file" >> "$output_file"
  # Add a newline to separate JSON objects
  echo >> "$output_file"
done

echo "All JSON files have been concatenated into $output_file"