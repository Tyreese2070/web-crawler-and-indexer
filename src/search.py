import sys
from src.indexer import Indexer

def print_word(indexer, word):
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

def find_query(indexer, query):
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