import requests
import json
from dotenv import dotenv_values

#url = "http://127.0.0.1:7001"
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
    #title_under = wikipedia_title.replace(" ", "_")
    title_spaces = wikipedia_title.replace("_", " ")
    #escape double quotes in the title
    title_spaces = title_spaces.replace('"', '\\"')
    query = (
        f"PREFIX schema: <http://schema.org/>\n"
        f"SELECT ?wikipedia_title ?wikidata_id WHERE {{\n"
        f'    VALUES ?wikipedia_title {{"{title_spaces}"@en}} .\n'
        f"    ?wikipedia_id schema:name ?wikipedia_title .\n"
        f"    ?wikipedia_id schema:about ?wikidata_id.\n"
        f"    ?wikipedia_id schema:isPartOf <https://en.wikipedia.org/> .\n"
        f"}}"
    )
    data = sparql_query(query)
    if "results" not in data or "bindings" not in data["results"]:
        print(query)
        raise ValueError(f"Error querying {wikipedia_title}")
    if len(data["results"]["bindings"]) == 0:
        return None
    else:
        if len(data["results"]["bindings"]) > 1:
            raise ValueError(f"Multiple entities found for {wikipedia_title}")
        else:
            return data["results"]["bindings"][0]["wikidata_id"]["value"]
        
def sparql_depicted_entities(qid):
    query = (
        f"PREFIX wd: <http://www.wikidata.org/entity/>\n"
        f"PREFIX wdt: <http://www.wikidata.org/prop/direct/>\n"
        f"SELECT ?depicted WHERE {{\n"
        "    VALUES ?p {wdt:P180}.\n"
        f"    wd:{qid} ?p ?depicted.\n"
        f"}}"
    )
    data = sparql_query(query)
    res=[]
    if "results" not in data or "bindings" not in data["results"]:
        raise ValueError(f"No results found for {qid}")
    for result in data["results"]["bindings"]:
        res.append(result["depicted"]["value"])
    return res


    