import argparse
import json
import paths


def main():

    # Read the JSON file
    with open(paths.ARTPEDIA2WIKI_PATH, 'r') as file:
        data = json.load(file)

    quid_set = set()
    # List all the keys in the JSON file
    for painting in data.values():
        depict=painting.get('P180',dict())
        for d in depict.keys():
            qid=d.split('/')[-1]
            quid_set.add(qid)
    with open(paths.ARTPEDIA_DEPICTED_IDS_FILTER_PATH, 'w') as file:
        for key in quid_set:
            file.write(f'{{"type":"item","id":"{key}"\n')

if __name__ == '__main__':
    main()
