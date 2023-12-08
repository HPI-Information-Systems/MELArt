
import argparse
import json
import os
from pathlib import Path
import urllib
import shutil

def main(args):
    #Read the list of image files from the folder el_candidates/images/combined

    folder_path = Path(args.images_folder)
    image_files = os.listdir(folder_path)

    #read the painintg images from artpedia2wiki_el.json

    discarded_images_folder = folder_path / 'discarded'
    discarded_images_folder.mkdir(parents=True, exist_ok=True)

    counter=0

    with open(args.file_path) as f:
        artpedia2wiki = json.load(f)
        for painting in artpedia2wiki.values():
            if painting['image_url'] is not None:
                image_urls = painting['image_url']
                for image_url in image_urls:
                    image_name = image_url.split('/')[-1]
                    image_name = urllib.parse.unquote(image_name)
                    if image_name in image_files and (folder_path / image_name).exists():
                        shutil.move(folder_path / image_name, discarded_images_folder / image_name)
                        counter += 1

    print(f"Moved {counter} images to discarded folder")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Checks candidate images and moves the ones that are paintings to a discarded folder')
    parser.add_argument('file_path', type=str, help='artpedia2wiki_el.json file path')
    parser.add_argument('images_folder', type=str, help='folder containing all candidate images')
    args = parser.parse_args()
    main(args)




