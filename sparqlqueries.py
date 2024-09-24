import time
from typing import Dict, List, Tuple, Union
import requests
from dotenv import dotenv_values

#url = "http://127.0.0.1:7001"
config = dotenv_values(".env")
url = config["QLEVER_API"]
agent = config["USER_AGENT"]

def sparql_request(query, accept="application/sparql-results+json"):
    global s
    headers = {
        "Accept": accept,
        "Content-type": "application/sparql-query",
        "User-Agent": agent
    }
    try:
        with requests.post(url, headers=headers, data=query) as response:
            return response
    except Exception as e:
        print("Connection error retrying in 30 seconds")
        time.sleep(30)
        response = requests.post(url, headers=headers, data=query)
        return response

def sparql_query(query):
    response = sparql_request(query, accept="application/sparql-results+json")
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

def sparql_all_lables(qids:Union[str,List[str]]) -> Union[Tuple[str,set],Dict[str,Tuple[str,set]]]:
    """
    Returns the main label and all alternative labels for a given QID or a list of QIDs
    """
    #if its a single qid, convert to list
    if not isinstance(qids, list):
        assert isinstance(qids, str)
        qids = [qids]

    wd_qids = [f"wd:{qid}" for qid in qids]

    query = (
        f"PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n"
        f"PREFIX wd: <http://www.wikidata.org/entity/>\n"
        f"SELECT ?qid ?label WHERE {{\n"
        f"    VALUES ?qid {{{" ".join(wd_qids)}}}\n"
        f"    ?qid rdfs:label ?label.\n"
        f"    FILTER (lang(?label) = 'en')\n"
        f"}}\n"
    )
    labels_dict=dict()
    for qid in qids:
        labels_dict[qid]=("",set())
    data = sparql_query(query)
    if "results" not in data or "bindings" not in data["results"]:
        raise ValueError(f"No results found for {qids}")
    for result in data["results"]["bindings"]:
        qid=result["qid"]["value"].split("/")[-1]
        label=result["label"]["value"]
        labels_dict[qid]=(label,set())
    #alternative labels
    query = (
        f"PREFIX skos: <http://www.w3.org/2004/02/skos/core#>\n"
        f"PREFIX wd: <http://www.wikidata.org/entity/>\n"
        f"SELECT ?qid ?altLabel WHERE {{\n"
        f"    VALUES ?qid {{{" ".join(wd_qids)}}}\n"
        f"    ?qid skos:altLabel ?altLabel.\n"
        f"    FILTER (lang(?altLabel) = 'en')\n"
        f"}}\n"
    )
    data = sparql_query(query)
    if "results" not in data or "bindings" not in data["results"]:
        raise ValueError(f"No results found for {qids}")
    for result in data["results"]["bindings"]:
        qid=result["qid"]["value"].split("/")[-1]
        labels_dict[qid][1].add(result["altLabel"]["value"])
    res=labels_dict if len(qids)>1 else labels_dict[qids[0]]
    return res

def sparql_descriptions(qids:Union[str,List[str]]) -> Union[Tuple[str,set],Dict[str,Tuple[str,set]]]:
    """
    Returns the english description for a given QID or a list of QIDs
    """
    #if its a single qid, convert to list
    if not isinstance(qids, list):
        assert isinstance(qids, str)
        qids = [qids]
    wd_qids = [f"wd:{qid}" for qid in qids]
    wd_qids_values = " ".join(wd_qids)

    query = "PREFIX schema: <http://schema.org/>\n" \
        "PREFIX wd: <http://www.wikidata.org/entity/>\n" \
        "SELECT ?qid ?desc WHERE { \n" \
        f"    VALUES ?qid {{{wd_qids_values}}} \n" \
        "    ?qid schema:description ?desc .\n" \
        "    FILTER (lang(?desc) = 'en')\n" \
        "}\n"
    
    descs_dict=dict()
    for qid in qids:
        descs_dict[qid]=""
    data = sparql_query(query)
    if "results" not in data or "bindings" not in data["results"]:
        print(query)
        raise ValueError(f"No results found for {qids}")
    for result in data["results"]["bindings"]:
        qid=result["qid"]["value"].split("/")[-1]
        desc=result["desc"]["value"]
        descs_dict[qid]=desc
    res=descs_dict if len(qids)>1 else descs_dict[qids[0]]
    return res

#get number of sitelinks for a given QID
def sparql_sitelinks(qids:Union[str,List[str]]) -> Union[int,Dict[str,int]]:
    #if its a single qid, convert to list
    if not isinstance(qids, list):
        assert isinstance(qids, str)
        qids = [qids]
    wd_qids = [f"wd:{qid}" for qid in qids]
    wd_qids_values = " ".join(wd_qids)

    query = "PREFIX schema: <http://schema.org/>\n" \
        "PREFIX wd: <http://www.wikidata.org/entity/>\n" \
        "PREFIX wikibase: <http://wikiba.se/ontology#>\n" \
        "SELECT ?qid ?sitelinks WHERE { \n" \
        f"    VALUES ?qid {{{wd_qids_values}}} \n" \
        "    ?node schema:about ?qid .\n" \
        "    ?node wikibase:sitelinks ?sitelinks .\n" \
        "}"
    
    sitelinks_dict=dict()
    for qid in qids:
        sitelinks_dict[qid]=0
    data = sparql_query(query)
    if "results" not in data or "bindings" not in data["results"]:
        print(query)
        raise ValueError(f"No results found for {qids}")
    for result in data["results"]["bindings"]:
        qid=result["qid"]["value"].split("/")[-1]
        count=int(result["sitelinks"]["value"])
        sitelinks_dict[qid]=count
    res=sitelinks_dict if len(qids)>1 else sitelinks_dict[qids[0]]
    return res

def get_all_qids(batch_size=1000,offset=0)->List[str]:
    sparql_qids="""PREFIX wikibase: <http://wikiba.se/ontology#>
    SELECT ?qid WHERE {
        ?qid a wikibase:Item.
    }
    """
    query=f"{sparql_qids} LIMIT {batch_size} OFFSET {offset}"
    RESPONSE=sparql_request(query, accept="text/csv")
    data=RESPONSE.text.split("\n")[1:]
    res=[]
    for line in data: # <http://www.wikidata.org/entity/Q100140262>
        #trim and remove the < > characters
        url_qid=line.strip()
        if url_qid:
            res.append(url_qid.split("/")[-1])
    return res

def count_qids():
    sparql_qids="""PREFIX wikibase: <http://wikiba.se/ontology#>
    SELECT (COUNT(?qid) AS ?count) WHERE {
        ?qid a wikibase:Item.
    }
    """
    data=sparql_query(sparql_qids)
    if "results" not in data or "bindings" not in data["results"]:
        raise ValueError(f"No results found for {sparql_qids}")
    return int(data["results"]["bindings"][0]["count"]["value"])

if __name__ == "__main__":
    #print(sparql_entity_qid("The Starry Night"))
    # print(sparql_all_lables("Q25931702"))
    # print(sparql_all_lables("Q5582"))
    # print(sparql_all_lables(["Q25931702","Q5582"]))

    # print(get_all_qids(10,0))
    # print(get_all_qids(10,10))
    # print(get_all_qids(10,1000000000000))

    # print(sparql_descriptions("Q25931702"))
    # print(sparql_descriptions("Q5582"))
    # print(sparql_descriptions(["Q1","Q25931702","Q5582"]))
    # print(sparql_descriptions("Q1"))

    # print(sparql_sitelinks(["Q1","Q25931702","Q5582"]))

    #generate a list of strings with Q1, Q2, ..., Q1000
    qids=[f"Q{i}" for i in range(1,501)]
    print(sparql_all_lables(qids))

    