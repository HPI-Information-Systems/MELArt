import requests
import json
from dotenv import dotenv_values

#url = "http://172.17.16.239:7001"
config = dotenv_values(".env")
url = config["QLEVER_API"]

def sparql_query(query):
    headers = {
        #"Accept": "application/qlever-results+json",
        "Accept": "application/sparql-results+json",
        "Content-type": "application/sparql-query"
    }

    response = requests.post(url, headers=headers, data=query)
    data = response.json()
    return data

def sparql_entity_qid(wikipedia_title):
    title_spaces = wikipedia_title.replace("_", " ")
    #title_underscores = wikipedia_title.replace(" ", "_")
    query = (
        f"PREFIX schema: <http://schema.org/>\n"
        f"SELECT ?wikipedia_title ?wikidata_id WHERE {{\n"
        f'    VALUES ?wikipedia_title {{"{title_spaces}"}} .\n'
        f"    ?wikipedia_id schema:name ?wikipedia_title .\n"
        f"    ?wikipedia_id schema:about ?wikidata_id.\n"
        f"    ?wikipedia_id schema:isPartOf <https://en.wikipedia.org/> .\n"
        f"}}"
    )
    data = sparql_query(query)
    if len(data["results"]["bindings"]) == 0:
        return None
    else:
        if len(data["results"]["bindings"]) > 1:
            raise ValueError(f"Multiple entities found for {wikipedia_title}")
        else:
            return data["results"]["bindings"][0]["wikidata_id"]["value"]

    