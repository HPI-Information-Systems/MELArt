import argparse
import json
import os
from tqdm import tqdm
import paths
import solrqueries as solrq
from tqdm import tqdm
import sparqlqueries as sq

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

    
    #save dictionary to json file
    file_path = paths.DICT_CANDIDATES_PATH

    if os.path.exists(file_path):
        print("Loading candidates from file, no need to search for them again")
        with open(file_path) as f:
            dict_candidates = json.load(f)

    else:
        for mention in tqdm(mentions_set, "Serching for candidates"):
            candidate_ids_relevance = set(solrq.solr_search(mention, rows=25))
            candidate_ids_popularity = set(solrq.solr_search(mention, rows=25, by_popularity=True))
            candidate_ids = list(candidate_ids_relevance.union(candidate_ids_popularity))
            dict_candidates[mention] = candidate_ids

        with open(file_path, 'w') as fp:
            json.dump(dict_candidates, fp)

    candidates_set = set()

    for candidate_ids in dict_candidates.values():
        candidates_set.update(candidate_ids)

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

    print(f"Only one candidate for {only_one_candidate} mentions")

    folder = paths.CANDIDATES_FOLDER_PATH

    for candidate_ids in tqdm(candidates_set):
        #request to wikidata to get the information about the candidate https://www.wikidata.org/w/rest.php/wikibase/v0/entities/items/Q7617093
        candidate_path=folder / f"{candidate_ids}.json"
        if not candidate_path.exists():
            candidate_summary = sq.summarize_qid(candidate_ids)
            res_obj = candidate_summary
            with open(candidate_path, 'w') as fp:
                json.dump(res_obj, fp)

    # iterate trough the json files in /el_candidates/ and extract the image urls into a set, then save the set in a text file line by line

    image_urls = set()

    for file in tqdm(os.listdir(folder)):
        path=folder / file
        if path.is_file() and path.suffix == ".json":
            with open(path) as f:
                data = json.load(f)
                images=data["images"]
                for image in images:
                    try:
                        commons_url = image
                        if not commons_url.startswith("http"):#from a different domain
                            image_urls.add(commons_url)
                    except:
                        pass

    with open(paths.CANDIDATES_IMAGES_TXT_PATH, 'w') as f:
        for item in image_urls:
            f.write("%s\n" % item)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get the candidates from wikidata, and build a file with all the images urls')
    parser.add_argument('--file_path', type=str, help='artpedia2wiki_matched.json file path', default=paths.ARTPEDIA2WIKI_MATCHED_PATH)
    args = parser.parse_args()
    main(args)



