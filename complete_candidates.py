
from urllib.parse import unquote
import paths as p
import json
import get_candidates
import get_img_urls

def main(args):

    dict_canditates = {}
    with open(p.CANDIDATES_FILE_PATH, 'r') as f:
        for line in f:
            entry = json.loads(line)
            dict_canditates[entry['qid']] = entry

    annotations = {}
    with open(p.MELART_ANNOTATIONS_PATH, 'r') as f:
        annotations = json.load(f)

    keys_matches = [
        "visual_el_matches",
        "contextual_el_matches",
    ]

    depiced = set()
    for ann in annotations.values():
        for key in keys_matches:
            for matches in ann[key]:
                for match in matches:
                    depiced.add(match['qid'])

    missing = depiced - set(dict_canditates.keys())
    print(f"Number of missing candidates: {len(missing)}")
    print("Some missing candidates:", list(missing)[:10])

    print("Extracting descriptions for missing candidates...")

    get_candidates.process_candidate_batch(list(missing))

    print("Extracting image URLs for missing candidates...")
    images = get_img_urls.process_candidate_batch([f"{qid}.json" for qid in missing])

    print(f"Number of image URLs found for missing candidates: {len(images)}")
    print(list(images))

    with open(p.IMAGES_TXT_PATH, 'a') as f:
        for image in images:
            f.write(f"{unquote(image)}\n")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Detect missing candidates in annotations")
    args = parser.parse_args()

    main(args)




