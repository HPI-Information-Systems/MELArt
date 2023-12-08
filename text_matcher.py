import spacy
from spacy.matcher import PhraseMatcher
import json
import argparse

from tqdm import tqdm

entities_dict = {}
count_visual_matches = 0
count_contextual_matches = 0
count_visual_sentence_matches = 0
count_contextual_sentence_matches = 0
paintings_with_matches = 0

def process_sentences(sentences, matcher, nlp):
    el_matches = []
    for i,sentence in enumerate(sentences):
        doc=nlp.make_doc(sentence)
        matches = matcher(doc, as_spans=True)
        el_matches_sentence = []
        for match in matches:
            el_matches_sentence.append({"qid": match.label_, "text": match.text, "start": match.start_char, "end": match.end_char})
        #remove matches contained in other matches
        #forst sort by start and length
        el_matches_sentence.sort(key=lambda x: (x['start'], x['start']-x['end']))
        to_remove = []
        for i, match in enumerate(el_matches_sentence):
            for j in range(i+1, len(el_matches_sentence)):
                if el_matches_sentence[j]['start'] >= match['start'] and el_matches_sentence[j]['end'] <= match['end']:
                    to_remove.append(j)
        to_remove = list(set(to_remove))
        to_remove.sort()
        to_remove.reverse()
        for i in to_remove:
            del el_matches_sentence[i]
        el_matches.append(el_matches_sentence)
    return el_matches

def process_painting(painting_qid, sentence_obj, nlp):
    global count_visual_matches
    global count_contextual_matches
    global count_visual_sentence_matches
    global count_contextual_sentence_matches
    global paintings_with_matches
    matcher = PhraseMatcher(nlp.vocab)
    new_sentence_obj = sentence_obj.copy()
    depicts = sentence_obj['P180']
    for key, value in depicts.items():
        qid = key.split('/')[-1]
        if qid in entities_dict and value[0].isupper():
            patterns = [nlp.make_doc(text) for text in entities_dict[qid]]
            matcher.add(key, patterns)
    sentences=sentence_obj['visual_sentences']
    visual_el_matches = process_sentences(sentences, matcher, nlp)    
    new_sentence_obj['visual_el_matches'] = visual_el_matches
    sentences=sentence_obj['contextual_sentences']
    contextual_el_matches = process_sentences(sentences, matcher, nlp)
    new_sentence_obj['contextual_el_matches'] = contextual_el_matches
    count_visual_matches += sum([len(matches) for matches in visual_el_matches])
    count_contextual_matches += sum([len(matches) for matches in contextual_el_matches])
    #count sentences
    count_visual_sentence_matches += sum([1 for matches in visual_el_matches if matches])
    count_contextual_sentence_matches += sum([1 for matches in contextual_el_matches if matches])
    if any([matches for matches in visual_el_matches]) or any([matches for matches in contextual_el_matches]):
        paintings_with_matches += 1
    return new_sentence_obj

def read_entities(entities_path):
    global entities_dict
    with open(entities_path) as f:
        for line in tqdm(f, desc="Reading entities file"):
            if line[-2] == ',':
                line = line[:-2]
            else:
                line = line[:-1]
            entity = json.loads(line)
            qid = entity['id']
            labels=[]
            if "en" in entity['labels']:
                labels.append(entity['labels']['en']['value'])
            if "en" in entity['aliases']:
                labels.extend([alias_obj["value"] for alias_obj in entity['aliases']['en']])
            #remove labels with no uppercase letter
            labels = [label for label in labels if any(c.isupper() for c in label)]
            #expand labels removing articles
            new_labels = []
            for label in labels:
                if label.startswith("The ") or label.startswith("the "):
                    new_labels.append(label[4:])
            labels.extend(new_labels)
            entities_dict[qid] = labels

def main(args):
    nlp = spacy.load("en_core_web_sm")
    read_entities(args.entities_path)
    file_path = args.file_path
    artpedia=json.load(open(file_path))
    new_artpedia = {}
    for qid, painting in tqdm(artpedia.items(), desc="Processing artpedia file"):
        new_artpedia[qid] = process_painting(qid, painting, nlp)
    
    with open(args.output_file, 'w') as f:
        json.dump(new_artpedia, f, indent=4)
    print("Visual matches: ", count_visual_matches)
    print("Contextual matches: ", count_contextual_matches)
    print("Visual sentence matches: ", count_visual_sentence_matches)
    print("Contextual sentence matches: ", count_contextual_sentence_matches)
    print("Paintings with matches: ", paintings_with_matches)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process sentences and label dictionary to output annotations in JSON format')
    parser.add_argument('file_path', type=str, help='artpedia2wiki.json file path')
    parser.add_argument('entities_path', type=str, help='ndjson file with all the information about the entities')
    parser.add_argument('output_file', type=str, help='path to output JSON file')
    args = parser.parse_args()
    main(args)


