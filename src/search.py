import sys
from src.indexer import Indexer

def print_word(indexer, word):
    tokens = indexer.tokenise(word)

    if not tokens:
        print("Invalid word")
        return
    
    word = tokens[0]
    if word in indexer.index:
        print(indexer.index[word])
    else:
        print(f"{word} not found in index")

def find_query(indexer, query):
    pass

def main():
    pass

if __name__ == "__main__":
    test_indexer = Indexer()
    test_indexer.load()
    print_word(test_indexer, "chicken")