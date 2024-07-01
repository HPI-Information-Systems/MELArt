import os
import json
from pathlib import Path
from tqdm import tqdm
import requests
import paths

candidates_folder = paths.CANDIDATES_FOLDER_PATH

# read all the candidate json files from el_candidates and put them in a dictionary
types_set=set()
for file in tqdm(candidates_folder.iterdir()):
    if not file.name.endswith('.json'):
        continue
    with open(file, 'r') as f:
        candidate = json.load(f)
        qid = file.name.split('.')[0]
        if candidate.get('statements', {}).get('P31'):
            for type in candidate['statements']['P31']:
                try:
                    type_qid = type["value"]["content"]
                    types_set.add(type_qid)
                except:
                    pass

# get the labels for all types from wikidata
types_dict = {}
for type in tqdm(types_set):
    url = f"https://www.wikidata.org/wiki/Special:EntityData/{type}.json"
    with requests.get(url) as response:
        data = json.loads(response.text)
        try:
            types_dict[type] = data['entities'][type]['labels']['en']['value']
        except:
            types_dict[type] = ""

# save to file
with open(paths.CANDIDATE_TYPES_DICT_PATH, 'w') as fp:
    json.dump(types_dict, fp)

                




