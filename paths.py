from pathlib import Path
import os

INPUT_FILES_PATH=Path("./input_files/")
ARTPEDIA_PATH=INPUT_FILES_PATH / "artpedia.json"
CURATED_ANNOTATIONS_PATH=INPUT_FILES_PATH / "curated_annotations.json"

AUX_OUTPUT_PATH=Path("./aux_files/")
#mkdir aux_files
os.makedirs(AUX_OUTPUT_PATH, exist_ok=True)

ARTPEDIA2WIKI_PATH=AUX_OUTPUT_PATH / "artpedia2wiki.json"
ARTPEDIA_DEPICTED_IDS_FILTER_PATH=AUX_OUTPUT_PATH / 'artpedia_depicted_ids_filter.txt'
ARTPEDIA_DEPICTED_ENTITIES_PATH=AUX_OUTPUT_PATH / 'artpedia_depicted_entities.ndjson'
ARTPEDIA2WIKI_MATCHED_PATH=AUX_OUTPUT_PATH / "artpedia2wiki_matched.json"
DICT_CANDIDATES_PATH=AUX_OUTPUT_PATH / "dict_candidates.json"

CANDIDATE_TYPES_DICT_PATH=AUX_OUTPUT_PATH / "candidate_types_dict.json"

OUTPUT_FILES_PATH=Path("./output_files/")
#mkdir output_files
os.makedirs(OUTPUT_FILES_PATH, exist_ok=True)
MELART_ANNOTATIONS_PATH=OUTPUT_FILES_PATH / "melart_annotations.json"

CANDIDATES_FOLDER_PATH=OUTPUT_FILES_PATH / "el_candidates"
os.makedirs(CANDIDATES_FOLDER_PATH, exist_ok=True)
CANDIDATES_IMAGES_PATH=CANDIDATES_FOLDER_PATH / "images"
os.makedirs(CANDIDATES_IMAGES_PATH, exist_ok=True)
CANDIDATES_IMAGES_TXT_PATH=CANDIDATES_IMAGES_PATH / "image_urls.txt"
