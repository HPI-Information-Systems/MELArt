import spacy
from spacy.matcher import PhraseMatcher
import json
import argparse
import paths
import sparqlqueries as sq

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
    for url in depicts:
        qid = url.split('/')[-1]
        if qid in entities_dict:
            labels=entities_dict[qid]
            #if any label starts wuth uppercase, add it to the matcher (we just keep named entities)
            if any([label[0].isupper() for label in labels]):
                patterns = [nlp.make_doc(text) for text in labels]
                matcher.add(qid, patterns)
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

def read_entity_labels(artpedia2wiki_obj):
    global entities_dict
    for qid, obj in tqdm(artpedia2wiki_obj.items(), desc="Reading entities file to get the labels"):
        for url in obj['P180']:
            qid=url.split('/')[-1]
            _, all_labels = sq.sparql_all_lables(qid)
            entities_dict[qid] = all_labels

def main(args):
    nlp = spacy.load("en_core_web_sm")
    file_path = args.file_path
    artpedia2wiki=json.load(open(file_path))
    read_entity_labels(artpedia2wiki)
    new_artpedia = {}
    for qid, painting in tqdm(artpedia2wiki.items(), desc="Processing artpedia file"):
        new_artpedia[qid] = process_painting(qid, painting, nlp)
    
    with open(args.output_file, 'w') as f:
        json.dump(new_artpedia, f, indent=4)
    print("Visual matches: ", count_visual_matches)
    print("Contextual matches: ", count_contextual_matches)
    print("Visual sentence matches: ", count_visual_sentence_matches)
    print("Contextual sentence matches: ", count_contextual_sentence_matches)
    print("Paintings with matches: ", paintings_with_matches)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process sentences and label dictionary to output annotations in JSON format', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--file_path', type=str, help='artpedia2wiki.json file path', default=paths.ARTPEDIA2WIKI_PATH)
    parser.add_argument('--output_file', type=str, help='path to output JSON file', default=paths.ARTPEDIA2WIKI_MATCHED_PATH)
    args = parser.parse_args()
    main(args)


