import os
import json
import pickle
import requests
import pandas as pd
import requests
from PIL import Image
from PIL import ImageFile
import argparse
ImageFile.LOAD_TRUNCATED_IMAGES = True
# Image.MAX_IMAGE_PIXELS = None

def dump_json(obj,save_path):
    print("dump "+save_path)
    with open(save_path, 'w') as outfile:
        json.dump(obj, outfile)

def load_json(file_path):
    file=open(file_path,"r")
    return json.load(file)
# image_dir="/home/linh/DATA/SIGIR2024/art_images/combined/"
# artpedia_json="/home/linh/DATA/SIGIR2024/artpedia.json"
#

def dump_json(obj,save_path):
    with open(save_path, 'w') as outfile:
        json.dump(obj, outfile)

def load_json(file_path):
    if os.path.exists(file_path):
        file=open(file_path,"r")
        return json.load(file)
    return {}

def download_image(url,fullname):
    # url = 'https://example/...'
    headers = {'User-Agent': 'CoolBot/0.0 (https://example.org/coolbot/; coolbot@example.org)'}
    # url=re.sub('/en/','/commons/',url)
    response = requests.get(url, headers=headers)

    print(response, url)
    try:
        response = requests.get(url, headers=headers)

        print(response,url)
        # urllib.request.urlretrieve(url,fullname)

    except:
        filename = open('/home/linh/DATA/SIGIR2024/artpedia/artpedia_notfound2.txt','a')
        filename.write(url+"\n")
        filename.close()


def download_img():
    filename = '/home/linh/DATA/SIGIR2024/artpedia/artpedia.json'

    annotation = json.load(open(filename, 'r'))
    for ann in annotation:
        img_url = annotation[ann]['img_url']

        download_image(img_url,'/home/linh/DATA/SIGIR2024/artpedia/images/'+img_url.split('/')[-1])
def download_notfound_img():
    not_found = open("/home/linh/DATA/SIGIR2024/artpedia/artpedia_notfound2.txt").readlines()
    not_found = [re.sub('\n', '', x) for x in not_found]
    for url in not_found:
        img_url =re.sub('/commons/','/en/',url)
        download_image(img_url, '/home/linh/DATA/SIGIR2024/artpedia/images/' + img_url.split('/')[-1])
# download_img()
# download_notfound_img()
def remove_not_found_in_json():
    filename = '/home/linh/DATA/SIGIR2024/artpedia/artpedia.json'
    img_folder='/home/linh/DATA/SIGIR2024/artpedia/images_resize/'
    annotation = json.load(open(filename, 'r'))
    removed_list=[]
    records=[]
    img_counter=0
    for ann in annotation:
        record=annotation[ann]
        img_url = record['img_url']
        img_name=img_url.split('/')[-1]
        if not os.path.exists(img_folder+img_name):
            removed_list.append(img_url)
        else:
            print("img_name",str(record)+";",img_name,img_counter)
            new_record={"caption":" ".join(record["visual_sentences"]),"image":"/scratch/user/uqlle6/code/artemo/LAVIS-main/art_data/images_resize/"+img_name,"image_id":img_counter,"id":img_counter,"instance_id":img_counter}
            # new_record={"caption":" ".join(record["visual_sentences"]),"image":img_folder+img_name,"image_id":img_counter,"id":img_counter,"instance_id":img_counter}
            records.append(new_record)
            img_counter+=1

    dump_json(records,"/home/linh/DATA/SIGIR2024/artpedia/coco_artpedia_train.json")
    test_eval_coco={"annotations":records[:10],"images":records[:10]}
    dump_json(test_eval_coco, "/home/linh/DATA/SIGIR2024/artpedia/coco_artpedia_test.json")
    dump_json(test_eval_coco, "/home/linh/DATA/SIGIR2024/artpedia/coco_artpedia_val.json")
    print("RECORDS LEN",len(records))
def rename_images():
    filename = '/home/linh/DATA/SIGIR2024/artpedia/artpedia.json'
    img_folder = '/home/linh/DATA/SIGIR2024/artpedia/images_resize/'
    annotation = json.load(open(filename, 'r'))
    removed_list = []
    records = []
    img_counter = 0
    for ann in annotation:
        record = annotation[ann]
        img_url = record['img_url']
        img_name = img_url.split('/')[-1]
        if not os.path.exists(img_folder + img_name):
            removed_list.append(img_url)
        else:
            print("img_name", img_name, img_counter)
            img_extension=img_name.split('.')[-1]
            new_record = {"caption": " ".join(record["visual_sentences"]), "image": img_folder + str(img_counter)+img_extension,
                          "image_id": img_counter, "id": img_counter, "instance_id": img_counter}
            records.append(new_record)
            os.rename(img_folder+img_name, img_folder + str(img_counter)+img_extension)
            img_counter += 1

def resize_artpedia_images():
    filename = '/home/linh/DATA/SIGIR2024/artpedia/artpedia.json'
    img_folder='/home/linh/DATA/SIGIR2024/artpedia/images/'
    resize_folder='/home/linh/DATA/SIGIR2024/artpedia/images_resize/'
    annotation = json.load(open(filename, 'r'))
    removed_list=[]
    records=[]
    img_counter=0
    big_counter=0
    big_list=[]
    for ann in annotation:
        record=annotation[ann]
        img_url = record['img_url']
        img_name=img_url.split('/')[-1]
        if not os.path.exists(img_folder+img_name):
            removed_list.append(img_url)
        else:
            try:
                new_record={"caption":" ".join(record["visual_sentences"]),"image":resize_folder+img_name,"image_id":img_counter}
                im = Image.open(img_folder+img_name)
                records.append(new_record)
                image_resized = im.resize((384, 384))
                # image_resized.save(resize_folder+img_name, quality=90)
                img_counter+=1
            except:
                big_image_folder="/home/linh/DATA/SIGIR2024/artpedia/big_images/"
                # shutil.move(img_folder+img_name,big_image_folder+img_name)
                big_counter+=1
                big_list.append(record)
        dump_json(big_list,"/home/linh/DATA/SIGIR2024/artpedia/big_images.json")



    print("big size images",big_counter)
def load(save_path):
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # path = dir_path + "/" + path
    if not os.path.exists(save_path):
        print("Not existed path",save_path)
        return None
    with open(save_path, 'rb') as file:
        return pickle.load(file)


    img_folder="/scratch/user/uqlle6/code/artemo/LAVIS-main/artemis_dataset/"
    images = glob.glob(os.path.join(img_folder, '*.*'))
    resize_folder='/scratch/user/uqlle6/code/artemo/dataset/artpedia/images512/resized_images/'
    images512=glob.glob(os.path.join(resize_folder, '*.png*'))
    img_counter=0
    # for image_path in images512:
    #         im = Image.open(image_path)
    #         img_name=image_path.split("/")[-1]
    #         image_resized = im.resize((384, 384))
    #         image_resized.save(resize_folder+img_name, quality=90)
    #         img_counter+=1
    # print("image512 resized",img_counter)
    img_counter=0
    error_file=open("/scratch/user/uqlle6/code/artemo/dataset/artemis_error_files.txt","w")
    for image_path in images:
        img_name = image_path.split("/")[-1].replace(".jpg", ".png")
        try:
            if not os.path.exists(resize_folder+img_name):
                print("not exists", image_path, img_counter)
                im = Image.open(image_path)
                img_name=image_path.split("/")[-1].replace(".jpg",".png")
                image_resized = im.resize((384, 384), Image.BICUBIC)
                if image_resized.mode == "CMYK":
                    print("CMYK",image_path,img_counter)
                    image_resized = image_resized.convert("RGB")

                image_resized.save(resize_folder+img_name, "PNG", optimize=True)
                # image_resized.save(resize_folder+img_name, quality=90)
                img_counter+=1
            else:
                print("remove:",image_path)
                os.remove(image_path)
        except:
            error_file.write(image_path+"\n")
            pass

    print("image jpg resized", img_counter)
    error_file.close()



def generate_query(entityid):
    return f"""
    SELECT ?description ?image ?movementLabel ?genreLabel ?creatorLabel ?depictsLabel WHERE {{
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
        wd:{entityid} wdt:P170 ?creator.
        ?creator rdfs:label ?creatorLabel FILTER (lang(?creatorLabel) = "en").
      }}
      OPTIONAL {{
        wd:{entityid} wdt:P180 ?depicts.
        ?depicts rdfs:label ?depictsLabel FILTER (lang(?depictsLabel) = "en").
      }}
    }}
    """


def get_wikidata_att_from_sparql(entity_id):
    query_string=generate_query(entity_id)
    from SPARQLWrapper import SPARQLWrapper2

    sparql = SPARQLWrapper2("http://example.org/sparql")
    sparql.setQuery(query_string)

    try:
        ret = sparql.query()
        print(ret.variables)  # this is an array consisting of "subj" and "prop"
        for binding in ret.bindings:
            # each binding is a dictionary. Let us just print the results
            print(f"{binding['subj'].value}, {binding['subj'].type}")
            print(f"{binding['prop'].value}, {binding['prop'].type}")
    except Exception as e:
        print(e)


def read_wiki_paintings():
    clean_data=load_json("/home/linh/DATA/SIGIR2024/clean_wiki.json")
    file1="/home/linh/DATA/SIGIR2024/entities/paintings_with_images_test_extension.ndjson"
    file2="/home/linh/DATA/SIGIR2024/entities/paintings_with_images_test.ndjson"
    file3="/home/linh/DATA/SIGIR2024/entities/paintings_with_images_train.ndjson"
    file4="/home/linh/DATA/SIGIR2024/entities/paintings_with_images_val.ndjson"
    file5="/home/linh/DATA/SIGIR2024/entities/paintings_with_images.ndjson"
    file6="/home/linh/DATA/SIGIR2024/splits/splits_lines_af"
    image2id=load_json("/home/linh/DATA/SIGIR2024/img2id.json")
    label2id=load_json("/home/linh/DATA/SIGIR2024/label2id.json")
    with open(file6) as f:
        data_test = [json.loads(l) for l in f.readlines()]
        data_counter=0
        for i in range(len(data_test)):
            item0=data_test[i]
            id=item0['id']
            if 'en' in item0['labels']:
                label=item0['labels']['en']['value']
                label2id[label]=id
            else:
                label=id
            if 'en' in item0['descriptions']:
                # print(item0['descriptions'])
                description=item0['descriptions']['en']['value']
            else:
                description=None
            #     print(item0['descriptions'])
            #     description=item0['descriptions'][list(item0['descriptions'])[0]]['value']
            P18_list=[]
            if 'P18' in  item0['claims']:
                for i in range(len(item0['claims']['P18'])):
                    if 'datavalue' in item0['claims']['P18'][i]['mainsnak']:
                        P18_list.append(item0['claims']['P18'][i]['mainsnak']['datavalue']['value'])#picture name
                        pic_name=item0['claims']['P18'][i]['mainsnak']['datavalue']['value']
                        image2id[pic_name]=id
                    # P18_value=item0['claims']['P18'][0]['mainsnak']['datavalue']['value']
            P31_value=item0['claims']['P31'][0]['mainsnak']['datavalue']['value']['id']#instance of
            P170_list=[]#creator
            if 'P170' in  item0['claims']:
                if 'datavalue' in item0['claims']['P170'][0]['mainsnak']:
                    P170_list.append(item0['claims']['P170'][0]['mainsnak']['datavalue']['value']['id'])#creator

            # P1679_value=item0['claims']['P1679'][0]['mainsnak']['datavalue']['value']#artwork id
            # P276_value=item0['claims']['P276'][0]['mainsnak']['datavalue']['value']#location
            # P186_value=item0['claims']['P186'][0]['mainsnak']['datavalue']['value']#made from material
            # P973_value=item0['claims']['P973'][0]['mainsnak']['datavalue']['value']#described at URL
            # P1476_value=item0['claims']['P1476'][0]['mainsnak']['datavalue']['value']#title text
            if 'P135' in item0['claims']:
                if 'datavalue' in item0['claims']['P135'][0]['mainsnak']:
                    P135_value=item0['claims']['P135'][0]['mainsnak']['datavalue']['value']#movement
                else:
                    P135_value=None
            else:
                P135_value=None
            if 'P136' in item0['claims']:
                if 'datavalue' in item0['claims']['P136'][0]['mainsnak']:
                    P136_value = item0['claims']['P136'][0]['mainsnak']['datavalue']['value']  # genre
                else:
                    P136_value=None
            else:
                P136_value=None
            P180_list=[]
            if 'P180' in item0['claims']:
                for i in range(len(item0['claims']['P180'])):
                    if 'datavalue' in item0['claims']['P180'][i]['mainsnak']:
                        P180_list.append(item0['claims']['P180'][i]['mainsnak']['datavalue']['value']['id'])
            clean_data[id] = {"description":description, "P18": P18_list, "P31": P31_value, "P135":P135_value,"P136":P136_value,"P180": P180_list}
            if len(P170_list):
                clean_data[id]["P170"] = P170_list
            data_counter+=1
    dump_json(clean_data,"/home/linh/DATA/SIGIR2024/clean_wiki.json")
    dump_json(image2id,"/home/linh/DATA/SIGIR2024/img2id.json")
    dump_json(label2id, "/home/linh/DATA/SIGIR2024/label2id.json")

def url_ok(url):
    # exception block
    try:

        # pass the url into
        # request.hear
        response = requests.head(url)

        # check the status code
        if response.status_code == 200:
            response=requests.get(url)
            content=response.json()
            print(content)
            page_id=list(content["query"]["pages"])[0]
            wiki_entity_id=content["query"]["pages"][page_id]['pageprops']['wikibase_item']
            print(wiki_entity_id)
            return True
        else:
            return False
    except requests.ConnectionError as e:
        return e
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

import requests

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
        "User-Agent": "YourAppName/0.1 (your@email.com)",  # Add your email or app name here
        "Accept": "application/sparql-results+json"
    }
    response = requests.get(endpoint_url, params={"query": query}, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

# if __name__ == "__main__":
#     entity_id = "Q12418"
#     query_string = generate_query(entity_id)
#     results = query_wikidata(query_string)
#     for result in results["results"]["bindings"]:
#         print(result)


def query_wikidata(query):
    endpoint_url = "https://query.wikidata.org/sparql"
    headers = {
        "User-Agent": "YourAppName/0.1 (linhlt.it.ee@gmail.com)",  # Add your email or app name here
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
def artpedia2wiki(artpedia_file,output_dir):
    from rapidfuzz import fuzz
    from wikimapper import WikiMapper
    mapper=WikiMapper("index_enwiki-latest.db")
    # filename = '/home/linh/DATA/SIGIR2024/artpedia/artpedia.json'

    annotation = json.load(open(artpedia_file, 'r'))

    clean_data=load_json(output_dir+"clean_wiki.json")
    art2wiki=load_json(output_dir+"artpedia2wiki.json")
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
        img_url = record['img_url']
        img_name = img_url.split('/')[-1]
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
                # print(art2wiki[id])

                #url_response=url_ok(img_url)
                #art2wiki[id]["url_exists"]=url_response
                #download_image(img_url, '/home/linh/DATA/SIGIR2024/artpedia/images/' + img_url.split('/')[-1])
        else:
            # print("NOT FOUND",title,counter)
            notfound+=1
        counter+=1
        # print(counter, img_url)
    dump_json(art2wiki,output_dir+"artpedia2wiki.json")
    # print("NOT FOUND", notfound)
# read_wiki_paintings()
# artpedia2wiki()
def extract_notfound():
        from wikimapper import WikiMapper

        filename = '/home/linh/DATA/SIGIR2024/artpedia/artpedia.json'

        annotation = json.load(open(filename, 'r'))

        notfound_list = {"The Finding of Erichthonius":"Q19892755",
                         "Recovery of San Juan de Puerto Rico by Governor Juan de Haro":"Q27700873",
                         "The Hunt in Aranjuez":"Q5965931",
                         "Charles II in armor":"Q24951450", "The Peace of Amiens (Ziegler)":"Q28004368",
                         "The Congress of Paris (Dubufe)":"Q17492872", "Jacob wrestling with the Angel (Delacroix)":"Q3837491"}

        for ann in annotation:
            record = annotation[ann]
            img_url = record['img_url']
            img_name = img_url.split('/')[-1]
            title = record["title"]
            # print("title",title)
            if title in notfound_list:
                print(ann, record)

def extract_entity_linking(record_i,sentence_type):
    ent_list=[]
    for sentence in record_i[sentence_type]:
        print(sentence)
        entities=list(record_i['P180'].values())
        doc =nlp(sentence)
        ent_dict={}
        try:
            for entity in entities:
                doc_entity=nlp(entity)
                name_mentions=[x.text for x in doc.noun_chunks ]
                # print(entity)
                # print(name_mentions)
                # link_ids=[doc_entity.similarity(nlp(x)) for x in name_mentions]
                link_ids=[]
                tokens_entity=[token.lemma_ for token in doc_entity if token.lemma_.lower() not in nlp.Defaults.stop_words and token.is_alpha]
                for name_mention in name_mentions:
                    tokens_name_mention=[token.lemma_ for token in nlp(name_mention) if token.lemma_.lower() not in nlp.Defaults.stop_words and token.is_alpha]
                    # print(tokens_entity,tokens_name_mention,len(set(tokens_entity).intersection(set(tokens_name_mention))))
                    similarity=len(set(tokens_entity).intersection(set(tokens_name_mention)))
                    link_ids.append(similarity)
                if link_ids and np.amax(link_ids)>0:
                    link_id=np.argmax(link_ids)
                else:
                    link_id=None
                ent_dict[entity]=name_mentions[link_id] if link_id!=None else {}
        except:
            pass
        print(ent_dict)
        ent_list.append(ent_dict)
    return  ent_list
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process an artpedia file and output results to a directory.")

    # Add arguments
    parser.add_argument("artpedia_file", type=str, help="The file path to the artpedia file.")
    parser.add_argument("output_dir", type=str, help="The directory where output should be saved.")

    # Parse the arguments
    args = parser.parse_args()
    artpedia2wiki(args.artpedia_file, args.output_dir)

# query_painting_by_id("Q614304")