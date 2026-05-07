import sys
from src.indexer import Indexer
import math
import difflib

def print_word(indexer: Indexer, word: str) -> None:
    """
    Normalises a word, looks it up in the index, and prints its statistics.
    
    Args: 
        indexer (Indexer): Loaded Indexer containing the web data
        word (str): The word to look up in the index
    """
    tokens = indexer.tokenise(word) # normalise the word

    if not tokens:
        print("Invalid word")
        return
    
    word = tokens[0]
    
    # Look up the word in the index and print the stats
    if word in indexer.index:
        print(f"Index for '{word}':")
        for url, data in indexer.index[word].items():
            print(f"    {url}")
            print(f"    Frequency: {data['frequency']}")
            print(f"    Positions: {data['positions']}")
            print(" ")
    else:
        print(f"'{word}' not found in index")

def find_query(indexer: Indexer, query: str) -> None:
    """
    Normalises a query, looks up each word in the index, and prints URLs
    that contain all the words in the query, ranked by their TF-IDF scores.

    Args: 
        indexer (Indexer): Loaded Indexer containing the web data
        query (str): The query to search for
    """

    tokens = indexer.tokenise(query)

    if not tokens:
        print("Invalid query")
        return
    
    for token in tokens:
        if token not in indexer.index:
            print("No pages found")
            suggestion = difflib.get_close_matches(token, indexer.index.keys(), n=1, cutoff=0.6)
            if suggestion:
                print(f"Did you mean: {suggestion[0]}")
            else:
                print(f"{token} not found in index")
            return
    
    matching_urls = set(indexer.index[tokens[0]].keys())
    for token in tokens[1:]:
        matching_urls.intersection_update(set(indexer.index[token].keys()))
    
    # Query suggestion if no pages found
    if not matching_urls:
        print("No pages found")
        return
    
    url_set = set()
    for word in indexer.index.values():
        url_set.update(word.keys())
    total_pages = len(url_set)

    ranked_results = {}
    for url in matching_urls:
        score = 0.0
        for token in tokens:
            tf = indexer.index[token][url]["frequency"]
            df = len(indexer.index[token])
            idf = math.log(total_pages / df) + 1
            score += tf * idf

        ranked_results[url] = score
    
    sorted_results = sorted(ranked_results.items(), key=lambda x: x[1], reverse=True)
    for rank, (url, score) in enumerate(sorted_results, start=1):
        print(f"{rank}. {url} (TF-IDF Score: {score:.3f})")
    print(" ")