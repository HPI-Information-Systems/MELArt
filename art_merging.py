import os
import json
import requests
import argparse
import paths
from dotenv import dotenv_values

config = dotenv_values(".env")
HTTP_AGENT=config["USER_AGENT"]

def dump_json(obj,save_path):
    with open(save_path, 'w') as outfile:
        json.dump(obj, outfile)

def load_json(file_path):
    if os.path.exists(file_path):
        file=open(file_path,"r")
        return json.load(file)
    return {}

def get_wiki_entityid(url):
        try:

            # pass the url into
            # request.hear
            response = requests.head(url)

            # check the status code
            if response.status_code == 200:
                response = requests.get(url)
                content = response.json()
                page_id = list(content["query"]["pages"])[0]
                wiki_entity_id = content["query"]["pages"][page_id]['pageprops']['wikibase_item']
                return wiki_entity_id

            else:
                return None
        except :
            return None

def generate_query(entityid):
    return f"""
    SELECT ?description ?image ?movementLabel ?genreLabel ?depicts ?depictsLabel ?creatorOfWork ?creatorOfWorkLabel WHERE {{
      OPTIONAL {{
        wd:{entityid} schema:description ?description FILTER (lang(?description) = "en").
      }}
      OPTIONAL {{
        wd:{entityid} wdt:P18 ?image.
      }}
      OPTIONAL {{
        wd:{entityid} wdt:P135 ?movement.
        ?movement rdfs:label ?movementLabel FILTER (lang(?movementLabel) = "en").
      }}
      OPTIONAL {{
        wd:{entityid} wdt:P136 ?genre.
        ?genre rdfs:label ?genreLabel FILTER (lang(?genreLabel) = "en").
      }}
      OPTIONAL {{
        wd:{entityid} wdt:P180 ?depicts.
        ?depicts rdfs:label ?depictsLabel FILTER (lang(?depictsLabel) = "en").
      }}
      OPTIONAL {{
        wd:{entityid} wdt:P170 ?creatorOfWork.
        ?creatorOfWork rdfs:label ?creatorOfWorkLabel FILTER (lang(?creatorOfWorkLabel) = "en").
      }}
    }}
    """

def query_wikidata(query):
    endpoint_url = "https://query.wikidata.org/sparql"
    headers = {
        "User-Agent": HTTP_AGENT,  # Add your email or app name here
        "Accept": "application/sparql-results+json"
    }
    response = requests.get(endpoint_url, params={"query": query}, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

def query_painting_by_id(entity_id):
    query_string = generate_query(entity_id)
    results = query_wikidata(query_string)
    record={"P135":"","P136":"","P180":{},"P170":{},"image_url":[]}
    for result in results["results"]["bindings"]:
        # print(result)
        if "movementLabel" in result:
            record["P135"] = result["movementLabel"]["value"]
        if "genreLabel" in result:
            record["P136"]=result["genreLabel"]["value"]
        if "depicts" in result and result["depicts"]["value"] not in record["P180"]:
            record["P180"][result["depicts"]["value"]]=result["depictsLabel"]["value"]
        if "creatorOfWork" in result and result["creatorOfWork"]["value"] not in record["P170"]:
            record["P170"][result["creatorOfWork"]["value"]]=result["creatorOfWorkLabel"]["value"]
        if 'image' in result:
            if result['image']['value'] not in record["image_url"]:
             record["image_url"].append(result['image']['value'])

    return record
def artpedia2wiki(artpedia_file):
    # from rapidfuzz import fuzz
    #from wikimapper import WikiMapper
    # mapper=WikiMapper("index_enwiki-latest.db")
    # filename = '/home/linh/DATA/SIGIR2024/artpedia/artpedia.json'

    annotation = json.load(open(artpedia_file, 'r'))

    #clean_data=load_json(output_dir+"clean_wiki.json")
    art2wiki=load_json(paths.ARTPEDIA2WIKI_PATH)
    counter=0
    notfound=0
    notfound_list = {"The Finding of Erichthonius": "Q19892755",
                     "Recovery of San Juan de Puerto Rico by Governor Juan de Haro": "Q27700873",
                     "The Hunt in Aranjuez": "Q5965931",
                     "Charles II in armor": "Q24951450", "The Peace of Amiens (Ziegler)": "Q28004368",
                     "The Congress of Paris (Dubufe)": "Q17492872",
                     "Jacob wrestling with the Angel (Delacroix)": "Q3837491"}

    for ann in annotation:
        record = annotation[ann]
        #img_url = record['img_url']
        #img_name = img_url.split('/')[-1]
        title=record["title"]

        url_id="https://en.wikipedia.org/w/api.php?action=query&prop=pageprops&titles="+title+"&format=json&redirects=1"

        entity_id=get_wiki_entityid(url_id)
        if title in notfound_list:
            entity_id=notfound_list[title]

        if entity_id:

                id=entity_id
                art2wiki[id]=query_painting_by_id(entity_id)
                art2wiki[id]["visual_sentences"]=record["visual_sentences"]
                art2wiki[id]["contextual_sentences"] = record["contextual_sentences"]
                art2wiki[id]["title"] = record["title"]
                art2wiki[id]["img_url"] = record["img_url"]
                art2wiki[id]["split"] = record["split"]
                art2wiki[id]["year"] = record["year"]
                if "P31" in art2wiki[id]:
                    if type(art2wiki[id]["P31"])==dict:
                        art2wiki[id]["P31"] = art2wiki[id]["P31"]["id"]
                if "P136" in art2wiki[id]:
                    if type(art2wiki[id]["P136"])==dict:
                        art2wiki[id]["P136"]=art2wiki[id]["P136"]["id"]
                if "P170" in art2wiki[id]:
                    P170_list=art2wiki[id]["P170"]
                    for j,item in enumerate(P170_list):
                        if type(item)==dict:
                            P170_list[j]=item['id']
                    art2wiki[id]["P170"]=P170_list
        else:
            notfound+=1
        counter+=1
    dump_json(art2wiki,paths.ARTPEDIA2WIKI_PATH)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process an artpedia file and output results to a directory.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # Add arguments
    parser.add_argument("--artpedia_file", type=str, help="The file path to the artpedia file.", default=str(paths.ARTPEDIA_PATH.absolute()))

    # Parse the arguments
    args = parser.parse_args()
    artpedia2wiki(args.artpedia_file)
