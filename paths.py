from pathlib import Path
import os

INPUT_FILES_PATH=Path("./input_files/")
ARTPEDIA_PATH=INPUT_FILES_PATH / "artpedia.json"
CURATED_ANNOTATIONS_PATH=INPUT_FILES_PATH / "curated_annotations.json"
WIKIPEDIA_DUMPS_PATH=INPUT_FILES_PATH / "enwiki"
WIKIPEDIA_PAGES_SQL_PATH=WIKIPEDIA_DUMPS_PATH / "enwiki-20240901-page.sql.gz"
WIKIPEDIA_REDIRECTS_SQL_PATH=WIKIPEDIA_DUMPS_PATH / "enwiki-20240901-redirect.sql.gz"

AUX_OUTPUT_PATH=Path("./aux_files/")
#mkdir aux_files
os.makedirs(AUX_OUTPUT_PATH, exist_ok=True)

ARTPEDIA2WIKI_PATH=AUX_OUTPUT_PATH / "artpedia2wiki.json"
ARTPEDIA_DEPICTED_IDS_FILTER_PATH=AUX_OUTPUT_PATH / 'artpedia_depicted_ids_filter.txt'
ARTPEDIA_DEPICTED_ENTITIES_PATH=AUX_OUTPUT_PATH / 'artpedia_depicted_entities.ndjson'
ARTPEDIA2WIKI_MATCHED_PATH=AUX_OUTPUT_PATH / "artpedia2wiki_matched.json"
ARTPEDIA2WIKI_DEPICTED_LABELS_PATH=AUX_OUTPUT_PATH / "artpedia2wiki_depicted_labels.json"
DICT_CANDIDATES_PATH=AUX_OUTPUT_PATH / "dict_candidates.json"
WIKIPEDIA_DUMP_FILES_PATH=AUX_OUTPUT_PATH / "enwiki"
#mkdir enwiki
os.makedirs(WIKIPEDIA_DUMP_FILES_PATH, exist_ok=True)
WIKIPEDIA_PAGES_CSV_PATH=WIKIPEDIA_DUMP_FILES_PATH / "enwiki-20240901-page.csv"
WIKIPEDIA_REDIRECTS_CSV_PATH=WIKIPEDIA_DUMP_FILES_PATH / "enwiki-20240901-redirect.csv"
ARTPEDIA_REDIRECTS_CSV_PATH=WIKIPEDIA_DUMP_FILES_PATH / "artpedia-20240901-redirect.csv"

CANDIDATE_TYPES_DICT_PATH=AUX_OUTPUT_PATH / "candidate_types_dict.json"

NOT_FOUND_IMAGES=AUX_OUTPUT_PATH / "not_found_images.txt"

CANDIDATES_FOLDER_PATH=AUX_OUTPUT_PATH / "el_candidates"
os.makedirs(CANDIDATES_FOLDER_PATH, exist_ok=True)

OUTPUT_FILES_PATH=Path("./output_files/")
#mkdir output_files
os.makedirs(OUTPUT_FILES_PATH, exist_ok=True)
MELART_ANNOTATIONS_PATH=OUTPUT_FILES_PATH / "melart_annotations.json"
MELART_AUTO_ANNOTATIONS_PATH=OUTPUT_FILES_PATH / "melart_automatic_annotations.json"

CANDIDATES_FILE_PATH=OUTPUT_FILES_PATH / "el_candidates.jsonl"

IMAGES_FOLDER_PATH=OUTPUT_FILES_PATH / "images"
IMAGES_FILES_FOLDER_PATH=IMAGES_FOLDER_PATH / "files"
os.makedirs(IMAGES_FILES_FOLDER_PATH, exist_ok=True)
IMAGES_TXT_PATH=IMAGES_FOLDER_PATH / "image_urls.txt"
