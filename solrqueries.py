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

def solr_search(query, rows=100):
    search_url = f"{solr_url}/select"
    params = {
        "q": query,
        "df": "label_txt_en",
        "fl": "qid",
        "rows": rows*50
    }
    response = requests.get(search_url, params=params)
    data = response.json()
    qid_list = []
    for doc in data["response"]["docs"]:
        qid=doc["qid"][0]
        if qid not in qid_list:
            qid_list.append(qid)
        if len(qid_list) >= rows:
            break
    return qid_list

if __name__ == "__main__":
    query = "apple"
    data = solr_search(query)
    print(data)