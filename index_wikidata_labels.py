import sparqlqueries as sq
import solrqueries as solrq
import argparse
from multiprocessing import Pool
from tqdm import tqdm
import utils

batch_size=1000

def process_batch(offset):
    try:
        qids=sq.get_all_qids(batch_size=batch_size, offset=offset)
        if len(qids)==0:
            return None
        labels=sq.sparql_all_lables(qids)
        site_links=sq.sparql_sitelinks(qids)
        documents = []
        for qid, (label,alt) in labels.items():
            #if no character in label or any of the alt labels is an uppercase letter, skip
            is_ne=utils.is_named_entiy((label,alt))
            # if not is_ne:
            #     #print(f"Skipping {qid} because no uppercase letter in label or alt labels")
            #     continue
            site_links_count=site_links[qid]
            doc={
                "id": qid,
                "qid_s": qid,
                "label_txt_en": label,
                "sitelinks_i": site_links_count,
                "is_ne_b": is_ne
            }
            if label:
                documents.append(doc)
            for i,label in enumerate(alt):
                id=f"{qid}_{i}"
                doc={
                    "id": id,
                    "qid_s": qid,
                    "label_txt_en": label,
                    "sitelinks_i": site_links_count,
                    "is_ne_b": is_ne
                }
                if label:
                    documents.append(doc)
        if len(documents)>0:
            solrq.solr_index_documents(documents)
    except Exception as e:
        print(f"Error processing batch {offset}: {e}")
        raise e

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Index the labels of all qids from wikidata into Solr')
    parser.add_argument('--batch_size', type=int, default=batch_size, help='Size of the batch to process')
    parser.add_argument('--workers', type=int, default=1, help='Number of workers to use')
    args = parser.parse_args()
    batch_size=args.batch_size
    total_qids=sq.count_qids()
    print(f"Total qids in Wikidata: {total_qids}")
    #max_qids=min(total_qids,1000) # TODO: remove this line
    max_qids=total_qids
    arguments = [(offset) for offset in range(0, max_qids, args.batch_size)]
    workers=args.workers
    #workers=4 # TODO: remove this line
    with Pool(workers) as p:
        for _ in tqdm(p.imap_unordered(process_batch, arguments), total=len(arguments)):
            pass
    solrq.solr_commit()