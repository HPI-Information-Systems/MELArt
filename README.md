# MELArt Dataset Generation

## Pre-requisites

### Configuration

1. Create a `.env` file (you can use `.env_sample` as a tempate) and set the access token for Wikimedia API and the user agent.
2. Install required libraries
3. Install spacy model `python -m spacy download en_core_web_sm`

### Input files
1. Create a folder called `input_files`.
2. Download the Artpedia dataset from [https://aimagelab.ing.unimore.it/imagelab/page.asp?IdPage=35](https://aimagelab.ing.unimore.it/imagelab/page.asp?IdPage=35) and place the `artpedia.json` file in the `input_files/` folder.
3. Download the Wikidata dump `latest-all.json.bz2` [https://dumps.wikimedia.org/wikidatawiki/entities/](https://dumps.wikimedia.org/wikidatawiki/entities/) the dump from 2023-03-22 was used to generate MELArt. The file should be put into or linked from `input_files/`.

You can also avoid having the `input_files/` folder, by adjusting the paths in the `paths.py` script.

## Dataset generation

1. `art_merging.py`: It matches Artpedia paintings to Wikidata entities using the Wikipedia title, and extracts painitng information from Wikidata.

2. `get_artpedia_depicted.sh`: This script first creates a text file to filter the Wikidata dump by qid, and then creates a ndjson file with the information from the depicted entities from the Wikidata dump.

3. `text_matcher.py`: matches the labels of the depcited entities in the visual and contextual sentences.


- text_matcher.py: matches the labels of the depcited entities in the visual and contextual sentences.

- build_candidate_desceiptions.py: build the textual descriptions from a set of json objects (one oine per candidate)

- get_candidates.py: get the candidates for the depicted entities in the visual and contextual sentences, using wikidata search API.

- crawl_images.py: crawl the images from the imgs_url file (from get_candidates.py) (requres dotenv file with the API key and [python-dotenv](https://github.com/theskumar/python-dotenv) package)