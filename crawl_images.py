import os
from pathlib import Path
import time
import requests
from tqdm import tqdm
from dotenv import dotenv_values
import argparse
import paths
import urllib.parse

wiki_access_token = None
headers = None

def get_wiki_image_url(wiki_image_path):
    wiki_image_path = urllib.parse.quote(wiki_image_path)
    api_url = f"https://api.wikimedia.org/core/v1/commons/file/File:{wiki_image_path}"
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return response.json()['preferred']['url']
    if response.status_code == 429:
        print("Too many requests")
        raise Exception("Too many requests")
    if response.status_code == 404:
        print(f"Image not found (404): {wiki_image_path}")
    return None

if __name__ == '__main__':
    config = dotenv_values(".env")
    if "WIKI_ACCESS_TOKEN" in config:
        wiki_access_token = config["WIKI_ACCESS_TOKEN"]
        headers = {
            "Authorization": f"Bearer {wiki_access_token}",
        }
        if "USER_AGENT" in config:
            headers["User-Agent"] = config["USER_AGENT"]
    parser = argparse.ArgumentParser(description="Crawl images from wikimedia commons based on a text file with the image names", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--input', type=str, help="File with the list of images to download", default=paths.IMAGES_TXT_PATH)
    args = parser.parse_args()
    
    input_path=Path(args.input)
    files_path=paths.IMAGES_FILES_FOLDER_PATH

    urls=[]
    not_found=[]
    with open(input_path,'r') as f:
        for line in tqdm(f.readlines()):
            line=line.strip()
            #get time now
            time_now=time.time()
            #if file exists, skip
            if line.startswith("http"):
                res_file=files_path / Path(line).name
            else:
                res_file=files_path / line.strip()
            if res_file.exists():
                continue
            os.makedirs(res_file.parent,exist_ok=True)
            url=line
            if not line.startswith("http"):
                url=get_wiki_image_url(line.strip())
            #compute how much time has elapsed
            if url:
                #download
                response = requests.get(url, stream=True, headers=headers)
                if response.status_code == 200:
                    with open(res_file, 'wb') as f:
                        response.raw.decode_content = True
                        f.write(response.content)
                elif response.status_code == 429:
                    print("Too many requests")
                    raise Exception("Too many requests")
                else:
                    print("Error downloading", url)
                    print(response.status_code)
                time_elapsed=time.time()-time_now
                time.sleep(max(0.8-time_elapsed,0))
            else:
                not_found.append(line)

    with open(paths.NOT_FOUND_IMAGES, 'w') as f:
        for item in not_found:
            f.write("%s\n" % item)
