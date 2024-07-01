#read a conll file with two columns, token and IOB tag and output a json file with the full sentece, and for each entity the start and end token and the entity type
import sys
import json
import re
from pathlib import Path
import paths
import random
random.seed(42)

matched_anns_path=paths.ARTPEDIA2WIKI_MATCHED_PATH
automatic_anns = json.load(open(matched_anns_path))

curated_anns_path=paths.CURATED_ANNOTATIONS_PATH
curated_anns=json.load(open(curated_anns_path))

test=set(curated_anns.keys())
train_val=set(automatic_anns.keys())-test
train_size=int(0.8*len(train_val))
train=set(random.sample(list(train_val), train_size))
val=train_val-train

#iterate artworks and assign the split. additionally replace the annotations for the test set with the all_anns information
for qid, artwork_info in automatic_anns.items():
    if qid in test:
        automatic_anns[qid]["split"]="test"
        for sentence in curated_anns[qid]:
            corresponding_list="visual_sentences" if sentence["sentence_type"]=="visual" else "contextual_sentences"
            #get the sentence index
            sentence_idx=artwork_info[corresponding_list].index(sentence["text"])
            corresponging_el_list="visual_el_matches" if sentence["sentence_type"]=="visual" else "contextual_el_matches"
            automatic_anns[qid][corresponging_el_list][sentence_idx]=[]
            for entity in sentence["entities"]:#{"start": 42,"end": 49,"qid": "Q345", "text": "Madonna"}
                #change to {"qid": "http://www.wikidata.org/entity/Q345","text": "Madonna","start": 42,"end": 49}
                full_entity={"qid": f"http://www.wikidata.org/entity/{entity['qid']}","text": entity["text"],"start": entity["start"],"end": entity["end"]}
                automatic_anns[qid][corresponging_el_list][sentence_idx].append(full_entity)
    elif qid in train:
        automatic_anns[qid]["split"]="train"
    elif qid in val:
        automatic_anns[qid]["split"]="val"
    else:
        print(f"Qid {qid} not found in any split")

new_path=paths.MELART_ANNOTATIONS_PATH
json.dump(automatic_anns, open(new_path, "w"), indent=2)






