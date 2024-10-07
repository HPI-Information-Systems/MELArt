# MELArt. A Multimodal Entity Linking  Dataset for Art

Code for the generation of MELArt. A Multimodal Entity Linking  Dataset for Art.

The code for the experiments with the baselines and for generating model-specific versions od the dataset can be found [here](https://github.com/HPI-Information-Systems/MELArt_experiments/)

## Pre-requisites

### Configuration

1. Create a `.env` file (you can use `.env_sample` as a tempate) and set the access token for Wikimedia API and the user agent.
2. Install required libraries. The easiest way is to use the provided conda environment `environment.yaml`
3. Install spacy English model `python -m spacy download en_core_web_sm`

### Input files

1. Download the Artpedia dataset from [https://aimagelab.ing.unimore.it/imagelab/page.asp?IdPage=35](https://aimagelab.ing.unimore.it/imagelab/page.asp?IdPage=35) and place the `artpedia.json` file in the `input_files/` folder.
<!-- 2. Download the Wikidata dump `latest-all.json.bz2` [https://dumps.wikimedia.org/wikidatawiki/entities/](https://dumps.wikimedia.org/wikidatawiki/entities/) the dump from 2023-03-22 was used to generate MELArt. The file should be put into or linked from `input_files/`. -->
<!-- TODO describe QLever setup -->
<!-- TODO describe Solr setup -->

You can also avoid having the `input_files/` folder, by adjusting the paths in the `paths.py` script.

## Dataset generation

Execute the following scripts to generate the dataset.

1. `convert_wikipedia_tables.sh`: This script converts the Wikipedia tables from the Wikidata dump to csv files. The output is stored in the `aux_files/` folder.

2. `art_merging.py`: It matches Artpedia paintings to Wikidata entities using the Wikipedia title, and extracts painting information from Wikidata.

3. `text_matcher.py`: Matches the labels of the depicted entities in the visual and contextual sentences.

4. `get_candidates.py`: Get the candidates for the depicted entities in the visual and contextual sentences, using Solr as a full text search engine. It creates a mention-candidates dictionary in the `aux_files/dict_candidates.json` file and for each candidate, it creates a json file with its information in the `aux_files/el_candidates` folder.

5. `get_img_urls.py`: Lists all the Wikimedia Commons file names or Wikipedia http urls needed to download the images. 

6. `crawl_images.py`: crawl the images from Wikimedia Commons and Wikipedia based on the `imgs_url.txt` file (from `get_img_urls.py`)

7. `filter_candidate_images.py`: Removes the candidate images that correspond to the paintings in MELArt.

8. `combine_curated_annotations.py`: This script combines the automatically generated annotations, with the manually curated annotations to produce the final dataset in the `output_files/melart_annotations.json` file.

9. `concat_candidates.py`: This script concatenates all the candidate files into a single `el_candidates.jsonl` file in the `output_files` folder.
