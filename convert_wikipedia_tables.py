import paths
from kwnlp_sql_parser import WikipediaSqlDump
import multiprocessing

""" Copilot generated description, checked by a human:
This script converts Wikipedia SQL dump files into CSV format. It uses the `kwnlp_sql_parser` library to parse the SQL dumps and extract specific columns. The script defines two main functions, `pages` and `redirects`, which handle the conversion of the pages and redirects SQL dumps, respectively. The multiprocessing module is used to run these functions in parallel, improving the efficiency of the conversion process.

Functions:
- pages(): Converts the Wikipedia pages SQL dump to a CSV file, keeping only the "page_id" and "page_title" columns for pages in the main namespace.
- redirects(): Converts the Wikipedia redirects SQL dump to a CSV file, keeping only the "rd_from" and "rd_title" columns for redirects in the main namespace.

The script is executed with a multiprocessing pool that runs the `pages` and `redirects` functions asynchronously.
"""

def pages():
    pages_path = paths.WIKIPEDIA_PAGES_SQL_PATH
    wsd = WikipediaSqlDump(
        pages_path.as_posix(),
        keep_column_names=["page_id", "page_title"],
        allowlists={"page_namespace": ["0"]})
    wsd.to_csv(paths.WIKIPEDIA_PAGES_CSV_PATH)

def redirects():
    redirects_path = paths.WIKIPEDIA_REDIRECTS_SQL_PATH
    wsd = WikipediaSqlDump(
        redirects_path.as_posix(),
        keep_column_names=["rd_from", "rd_title"],
        allowlists={"rd_namespace": ["0"]})
    wsd.to_csv(paths.WIKIPEDIA_REDIRECTS_CSV_PATH)

if __name__ == "__main__":
    with multiprocessing.Pool(2) as pool:
        pool.apply_async(pages)
        pool.apply_async(redirects)
        pool.close()
        pool.join()