# MELArt

- art_merging.py: convert original artpedia, augmenting with the painting's wikidata information. It matches from paintings to wikidata entities using the wikipedia title.

- text_matcher.py: matches the labels of the depcited entities in the visual and contextual sentences.

- build_candidate_desceiptions.py: build the textual descriptions from a set of json objects (one oine per candidate)

- get_candidates.py: get the candidates for the depicted entities in the visual and contextual sentences, using wikidata search API.

- crawl_images.py: crawl the images from the imgs_url file (from get_candidates.py) (requres dotenv file with the API key and [python-dotenv](https://github.com/theskumar/python-dotenv) package)