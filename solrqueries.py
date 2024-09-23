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