import requests
import json
from dotenv import dotenv_values

config = dotenv_values(".env")
solr_url = config["SOLR_CORE_API"]

def solr_index_documents(docs):
    update_url = f"{solr_url}/update"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(update_url, headers=headers, data=json.dumps(docs))
    if response.status_code != 200:
        print(f"Failed to index documents {[doc["id"] for doc in docs]}: {response.text}")

def solr_commit():
    commit_url = f"{solr_url}/update?commit=true"
    requests.get(commit_url)

def solr_search(query, rows=100, by_popularity=False):
    search_url = f"{solr_url}/select"
    sort_field="sitelinks_i desc" if by_popularity else "score desc, sitelinks_i desc"
    params = {
        "q": query,
        "df": "label_txt_en",
        "fl": "qid_s",
        "fq": "{!collapse field=qid_s}",
        "sort": sort_field,
        "rows": rows
    }
    response = requests.get(search_url, params=params)
    data = response.json()
    qid_list = []
    for doc in data["response"]["docs"]:
        qid=doc["qid_s"]
        qid_list.append(qid)
    return qid_list

def solr_is_present(qid):
    search_url = f"{solr_url}/select"
    params = {
        "q": "*:*",
        "fq": f"qid_s:{qid}",
        "fl": "qid_s",
        "rows": 1
    }
    response = requests.get(search_url, params=params)
    data = response.json()
    return len(data["response"]["docs"]) > 0

if __name__ == "__main__":
    query = "Mary"
    data = solr_search(query)
    print(data)
    data = solr_search(query, by_popularity=True)
    print(data)
    print(solr_is_present("Q345"))