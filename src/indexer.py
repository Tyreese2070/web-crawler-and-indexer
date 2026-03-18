import json
import string
import os

from crawler import crawl

class Indexer:
    def __init__(self):
        self.index = {}
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.filepath = os.path.abspath(os.path.join(current_dir, "..", "data", "index.json"))

    def tokenise(self, text):
        """
        Convert text to lowercase, remove punctuation, and split into tokens
        """
        text = text.lower()
        text = text.translate(str.maketrans("", "", string.punctuation))
        tokens = text.split()
        return tokens

    def build(self, pages):
        """
        Build inverted index from parsed pages 
        """
        for page in pages:
            url = page["url"]
            text = page["text"]
            words = self.tokenise(text)

            for position, word in enumerate(words):
                if word not in self.index:
                    self.index[word] = {}
                
                if url not in self.index[word]:
                    self.index[word][url] = {"frequency": 0, "positions": []}
                
                self.index[word][url]["frequency"] += 1
                self.index[word][url]["positions"].append(position)
    
    def save(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)

        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.index, f, ensure_ascii=False, indent=4)

    def load(self):
        """Load index from JSON file"""
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                self.index = json.load(f)
        except FileNotFoundError:
            print("Index file not found.")