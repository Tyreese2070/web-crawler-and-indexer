import sys
from src.indexer import Indexer

def print_word(indexer: Indexer, word: str) -> None:
    """
    Normalises a word, looks it up in the index, and prints its statistics.
    
    Args: 
        indexer (Indexer): Loaded Indexer containing the web data
        word (str): The word to look up in the index
    """
    tokens = indexer.tokenise(word)

    if not tokens:
        print("Invalid word")
        return
    
    word = tokens[0]
    
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
    that contain all the words in the query.

    Args: 
        indexer (Indexer): Loaded Indexer containing the web data
        query (str): The query to search for
    """

    tokens = indexer.tokenise(query)

    if not tokens:
        print("Invalid query")
        return
    
    if tokens[0] not in indexer.index:
        print("No pages found")
        return
    
    matching_urls = set(indexer.index[tokens[0]].keys())

    for token in tokens[1:]:
        if token not in indexer.index:
            matching_urls = set()
            break
        matching_urls.intersection_update(set(indexer.index[token].keys()))

    if not matching_urls:
        print("No pages found")
    else:
        for url in matching_urls:
            print(url)