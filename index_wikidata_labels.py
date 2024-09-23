import os
import time
import sparqlqueries as sq
import solrqueries as solrq
import argparse
from multiprocessing import Pool
from tqdm import tqdm

batch_size=100

def process_batch(offset):
    try:
        qids=sq.get_all_qids(batch_size=batch_size, offset=offset)
        if len(qids)==0:
            return None
        labels=sq.sparql_all_lables(qids)
        documents = []
        for qid, (label,alt) in labels.items():
            #if no character in label or any of the alt labels is an uppercase letter, skip
            if not any(c.isupper() for c in label) and not any(any(c.isupper() for c in alt_label) for alt_label in alt):
                #print(f"Skipping {qid} because no uppercase letter in label or alt labels")
                continue
            
            doc={
                "id": qid,
                "qid": qid,
                "label_txt_en": label
            }
            documents.append(doc)
            for i,label in enumerate(alt):
                id=f"{qid}_{i}"
                doc={
                    "id": id,
                    "qid": qid,
                    "label_txt_en": label
                }
                documents.append(doc)
        solrq.solr_index_documents(documents)
    except Exception as e:
        print(f"Error processing batch {offset}: {e}")
        raise e

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Index the labels of all qids from wikidata into Solr')
    parser.add_argument('--batch_size', type=int, default=batch_size, help='Size of the batch to process')
    #parser.add_argument('--max', type=int, help='Max number of qids to process, if not set, all qids will be processed')
    parser.add_argument('--workers', type=int, default=os.cpu_count(), help='Number of workers to use')
    args = parser.parse_args()
    total_qids=sq.count_qids()
    print(f"Total qids in Wikidata: {total_qids}")
    #max_test=100000 # TODO: remove this line
    #max_qids=min(total_qids,max_test)
    max_qids=total_qids
    arguments = [(offset) for offset in range(0, max_qids, args.batch_size)]
    workers=args.workers
    #workers=4 # TODO: remove this line
    with Pool(workers) as p:
        #p.map(process_batch, arguments)
        for _ in tqdm(p.imap_unordered(process_batch, arguments), total=len(arguments)):
            pass
    solrq.solr_commit()