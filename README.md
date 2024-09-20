# MELArt. A Multimodal Entity Linking  Dataset for Art.

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

You can also avoid having the `input_files/` folder, by adjusting the paths in the `paths.py` script.

## Dataset generation

Execute the following scripts to generate the dataset.

1. `convert_wikipedia_tables.sh`: This script converts the Wikipedia tables from the Wikidata dump to a more readable format. The output is stored in the `aux_files/` folder.

2. `art_merging.py`: It matches Artpedia paintings to Wikidata entities using the Wikipedia title, and extracts painting information from Wikidata.

3. `text_matcher.py`: Matches the labels of the depicted entities in the visual and contextual sentences.

4. `get_candidates.py`: Get the candidates for the depicted entities in the visual and contextual sentences, using Wikidata search API. For each candidate, it creates a json file with its information in the `aux_files/el_candidates` folder. Also creates a file with the list of entity image paths.

5. `get_candidate_types.py`: Reads each candidate information, builds a set of all the types, and uses Wikidata's API to get the type labels. The types information is stored in the `aux_files/candidate_types_dict.json` file.

6. `crawl_images.py`: crawl the images from Wikimedia Commons based on the `imgs_url.txt` file (from get_candidates.py)

7. `filter_candidate_images`: Removes the candidate images that correspond to the paintings in MELArt.

8. `combine_curated_annotations`: This script combines the automatically generated annotations, with the manually curated annotations to produce the final dataset in the `output_files/melart_annotations.json` file.