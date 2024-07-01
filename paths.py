from pathlib import Path
import os

INPUT_FILES_PATH=Path("./input_files/")
ARTPEDIA_PATH=INPUT_FILES_PATH / "artpedia.json"

AUX_OUTPUT_PATH=Path("./aux_files/")
#mkdir aux_files
os.makedirs(AUX_OUTPUT_PATH, exist_ok=True)

ARTPEDIA2WIKI_PATH=AUX_OUTPUT_PATH / "artpedia2wiki.json"
ARTPEDIA_DEPICTED_IDS_FILTER_PATH=AUX_OUTPUT_PATH / 'artpedia_depicted_ids_filter.txt'
ARTPEDIA_DEPICTED_ENTITIES_PATH=AUX_OUTPUT_PATH / 'artpedia_depicted_entities.ndjson'

OUTPUT_FILES_PATH=Path("./output_files/")
#mkdir output_files
os.makedirs(OUTPUT_FILES_PATH, exist_ok=True)
