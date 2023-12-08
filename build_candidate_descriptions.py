import argparse
from multiprocessing import Pool
from typing import Dict, List, Tuple
import json
import tqdm
from pathlib import Path

p_ids = []

def get_desc(line: str) -> Tuple[str,str]:
    """
    Build a description from the json line concatenating the labels and aliases and the description
    """
    obj_ids = []
    try:
        #remove trailing \n
        line = line.strip()
        if line[-1] == ',':
            line = line[:-1]
        # Load the json line
        line_json = json.loads(line)
        # Get the id
        obj_id = line_json['id']
        # Get the labels in english
        labels = line_json['labels']
        desc=[]
        if "en" in labels:
            label = labels['en']['value']
            desc.append(label)
        # Get the aliases in english
        aliases = line_json['aliases']
        if "en" in aliases:
            for alias in aliases['en']:
                desc.append(alias['value'])
        # Get the description in english
        descriptions = line_json['descriptions']
        if "en" in descriptions:
            desc.append(descriptions['en']['value'])
        # Build the description
        desc = '. '.join(desc)
        return (obj_id, desc)
    except Exception as e:
        print(e)
        #pretty print the line
        with open('error.json', 'w') as f:
            json.dump(json.loads(line), f, indent=4)
        raise e

if __name__ == '__main__':
    # Get the command line arguments
    parser = argparse.ArgumentParser(description='Get the object ids from the wikidata json lines give the predicate ids')
    #add description in the argument parser
    #parser.add_help()
    #predicate ids as a list
    parser.add_argument('--input', required=True, help='Input file (json lines)')
    parser.add_argument('--output', help='Output file (json lines))')
    parser.add_argument('--num-processes', type=int, default=1, help='Number of processes to use')
    args = parser.parse_args()

    lines=[]
    # Read the input file
    with open(args.input, 'r') as f:
        lines = f.readlines()

    all_desc = dict()

    #process with Pool
    with Pool(args.num_processes) as pool:
        #process with tqdm and imap
        for (k,v) in tqdm.tqdm(pool.imap(get_desc, lines, chunksize=min(len(lines),16)), total=len(lines)):
            all_desc[k] = v

    if args.output:
        # Write the output file
        with open(args.output, 'w') as f:
            json.dump(all_desc, f)
    else:
        # add _desc to the input file
        p=Path(args.input)
        with open(p.parent / (p.stem + '_desc' + p.suffix), 'w') as f:
            json.dump(all_desc, f)
        

    print(f'Number of object ids: {len(all_desc)}')
    