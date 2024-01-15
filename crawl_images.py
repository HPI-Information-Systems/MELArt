import os
from pathlib import Path
import time
import requests
from tqdm import tqdm
from dotenv import dotenv_values
import argparse


wiki_access_token = None
headers = None

def get_wiki_image_url(wiki_image_path):
    api_url = f"https://api.wikimedia.org/core/v1/commons/file/File:{wiki_image_path}"
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return response.json()['preferred']['url']
    if response.status_code == 429:
        print("Too many requests")
        raise Exception("Too many requests")

if __name__ == '__main__':
    config = dotenv_values(".env")
    if "WIKI_ACCESS_TOKEN" in config:
        wiki_access_token = config["WIKI_ACCESS_TOKEN"]
        headers = {
            "Authorization": f"Bearer {wiki_access_token}",
        }
        if "USER_AGENT" in config:
            headers["User-Agent"] = config["USER_AGENT"]
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    args = parser.parse_args()
    
    input_path=Path(args.input)
    base_path=input_path.parent

    urls=[]
    with open(args.input,'r') as f:
        for line in tqdm(f.readlines()):
            #get time now
            time_now=time.time()
            #if file exists, skip
            res_file=base_path / "combined" / line.strip()
            if res_file.exists():
                continue
            os.makedirs(res_file.parent,exist_ok=True)
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