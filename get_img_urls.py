import argparse
import json
import os
from tqdm import tqdm
import paths
from tqdm import tqdm
from multiprocessing import Pool
from pathlib import Path
from urllib.parse import unquote
import utils

batch_size=100
workers=8

commons_prefix=utils.commons_prefix
commons_prefix_len=len(commons_prefix)

def process_candidate_batch(candidate_files):
    folder = paths.CANDIDATES_FOLDER_PATH
    image_urls = set()
    for candidate_file in candidate_files:
        candidate_path=folder / candidate_file
        with open(candidate_path, 'r') as f:
            data = json.load(f)
            images=data["images"]
            for image in images:
                try:
                    commons_url = image
                    #http://commons.wikimedia.org/wiki/Special:FilePath/T%C3%B6%C3%B6l%C3%B6nlahti1.jpg
                    if commons_url.startswith(commons_prefix):#from a different domain
                        file_name = commons_url[commons_prefix_len:]
                        image_urls.add(file_name)
                except:
                    pass
    return image_urls

def main(args):

    batch_size=args.batch_size
    workers=args.workers

    image_urls = []

    candidates_folder = paths.CANDIDATES_FOLDER_PATH

    json_file_names = [f for f in os.listdir(candidates_folder) if f.endswith('.json')]

    #split the list of json files into batches
    json_file_names = [json_file_names[i:i + batch_size] for i in range(0, len(json_file_names), batch_size)]

    with Pool(workers) as p:
        for urls in tqdm(p.imap_unordered(process_candidate_batch, json_file_names), total=len(json_file_names), desc="Processing candidates in batches"):
            image_urls.extend(urls)

    artpedia_matches = paths.ARTPEDIA2WIKI_MATCHED_PATH
    with open(artpedia_matches, 'r') as f:
        artpedia_matches = json.load(f)

    for qid, obj in artpedia_matches.items():
        img_url = obj.get('img_url')
        #get the file name from the url
        if img_url.startswith(utils.commons_prefix):
            img_url = Path(img_url).name
        image_urls.append(img_url)

    image_urls = set(image_urls)

    #url decode the names (for instance Albert%20II%20of%20Austria.jpg -> Albert_II_of_Austria.jpg)
    image_urls = {unquote(url) for url in image_urls}

    #sort the set
    image_urls = sorted(image_urls)

    with open(paths.IMAGES_TXT_PATH, 'w') as f:
        for item in image_urls:
            f.write("%s\n" % item)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get the candidates from wikidata, and build a file with all the images urls')
    parser.add_argument('--batch_size', type=int, default=batch_size, help='Batch size for processing candidates')
    parser.add_argument('--workers', type=int, default=workers, help='Number of worker processes to use')
    args = parser.parse_args()
    main(args)



