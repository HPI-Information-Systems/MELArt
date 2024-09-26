
import argparse
import json
import os
from pathlib import Path
import urllib
import shutil
from urllib.parse import unquote

from tqdm import tqdm
import paths

def main(args):

    artpedia_matches_path = Path(args.file_path)
    artpedia_matches=json.load(open(artpedia_matches_path,"r"))

    image_urls = set()

    for qid, obj in artpedia_matches.items():
        img_url = obj.get('img_url')
        #get the file name from the url
        img_url = Path(img_url).name
        image_urls.add(img_url)

    #url decode the names (for instance Albert%20II%20of%20Austria.jpg -> Albert_II_of_Austria.jpg)
    image_urls = {unquote(url) for url in image_urls}

    candidates_folder = Path(args.candidates_folder)

    commons_prefix="http://commons.wikimedia.org/wiki/Special:FilePath/"
    commons_prefix_len=len(commons_prefix)

    for candidate_file in tqdm(os.listdir(candidates_folder), desc="Processing candidates"):
        if candidate_file.endswith('.json'):
            remove = False
            with open(candidates_folder / candidate_file, 'r') as f:
                data = json.load(f)
                images = data["images"]
                for image in images:
                    commons_url = image
                    file_name = commons_url[commons_prefix_len:]
                    file_name = unquote(file_name)
                    if file_name in image_urls:
                        images.remove(image)
                        remove = True
                data["images"] = images
            if remove:
                with open(candidates_folder / candidate_file, 'w') as f:
                    json.dump(data, f)
                print(f"Removed image from {candidate_file}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Checks candidate images and moves the ones that are paintings to a discarded folder')
    parser.add_argument('--file_path', type=str, help='artpedia2wiki_matched.json file path', default=paths.ARTPEDIA2WIKI_MATCHED_PATH)
    parser.add_argument('--candidates_folder', type=str, help='folder containing all candidate json files', default=paths.CANDIDATES_FOLDER_PATH)
    args = parser.parse_args()
    main(args)




