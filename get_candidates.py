import argparse
from pathlib import Path
import requests
import json
import os
from tqdm import tqdm

def main(args):

    # Read the artpedia.json file
    with open(args.file_path) as file:
        data = json.load(file)

    # Create an empty set to store the mentions
    mentions_set = set()

    ground_truth_qids = set()

    # Iterate over each element in the data
    for element in data.values():
        for matches_fiels in ['visual_el_matches', 'contextual_el_matches']:
            for match in element[matches_fiels]:
                for v in match:
                    # Add the mention to the set
                    mentions_set.add(v['text'])
                    match_qid_url=v['qid']
                    match_qid=match_qid_url.split('/')[-1]
                    ground_truth_qids.add(match_qid)

    dict_candidates = {}

    for mention in mentions_set:
        #make an http request to wbsearchentities in wikidata
        #https://www.wikidata.org/w/api.php?action=wbsearchentities&format=json&language=en&type=item&continue=0&search=Madonna&limit=50
        url=f"https://www.wikidata.org/w/api.php?action=wbsearchentities&format=json&language=en&type=item&continue=0&search={mention}&limit=50"
        response = requests.get(url)
        res_obj = response.json()
        search_res_obj = res_obj.get('search',[])
        candidate_ids = []
        for res in search_res_obj:
            candidate_ids.append(res['id'])
        dict_candidates[mention] = candidate_ids
        

    #save dictionary to json file
    file_path = Path('data_files/dict_candidates.json')
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, 'w') as fp:
        json.dump(dict_candidates, fp)

    candidates_set = set()

    for candidate_ids in dict_candidates.values():
        candidates_set.update(candidate_ids[:20])

    candidates_set.update(ground_truth_qids)

    lengths=[]
    for candidate_ids in dict_candidates.values():
        lengths.append(len(candidate_ids))

    #average number of candidates per mention
    sum(lengths)/len(lengths)

    only_one_candidate = 0
    for candidate_ids in dict_candidates.values():
        if len(candidate_ids) == 1:
            only_one_candidate+=1

    only_one_candidate

    folder = Path("data_files/el_candidates/")

    for candidate_ids in tqdm(candidates_set):
        #request to wikidata to get the information about the candidate https://www.wikidata.org/w/rest.php/wikibase/v0/entities/items/Q7617093
        if not Path(f"{folder}/{candidate_ids}.json").exists():
            url=f"https://www.wikidata.org/w/rest.php/wikibase/v0/entities/items/{candidate_ids}"
            response = requests.get(url)
            res_obj = response.json()
            with open(f"{folder}/{candidate_ids}.json", 'w') as fp:
                json.dump(res_obj, fp)

    # iterate trouh the json files in /el_candidates/ and extract the image urls into a set, then save the set in a text file line by line

    image_urls = set()

    for file in tqdm(os.listdir(folder)):
        path=folder / file
        if path.is_file() and path.suffix == ".json":
            with open(path) as f:
                data = json.load(f)
                if data.get('statements', {}).get('P18'):
                    for image in data['statements']['P18']:
                        try:
                            commons_url = image["value"]["content"]
                            if not commons_url.startswith("http"):#from a different domain
                                image_urls.add(commons_url)
                        except:
                            pass

    images_folder = folder / "images"
    images_folder.mkdir(parents=True, exist_ok=True)

    with open(images_folder / "image_urls.txt", 'w') as f:
        for item in image_urls:
            f.write("%s\n" % item)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get the candidates from wikidata, and build a file with all the images urls')
    parser.add_argument('file_path', type=str, help='artpedia2wiki_el.json file path')
    args = parser.parse_args()
    main(args)



