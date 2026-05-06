# web-crawler-and-indexer
![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)

# Overview
A command line web crawler, indexer, and search engine. The tool recursively crawls the given website with a 6 second politeness window, and parses the HTML content to build an inverted index. 

This also includes some additional features such as intersections, TF-IDF ranking, and query suggestions

# Installation and Setup
**Requires Python 3.12 or higher.**
**Developed using Python 3.14.**

```bash
git clone https://github.com/Tyreese2070/web-crawler-and-indexer
cd web-crawler-and-indexer

# Windows:
python -m venv venv
.\venv\Scripts\activate

# Linux / MacOS:
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

# Usage
```bash
python -m src.main
```

## Example CLI Session:
Commands: build, load, print <word>, find <query>, exit

> build
Crawling and building index
Building index
Built and saved index
> 

> load
Index loaded
> 

> print hello
'hello' not found in index
> print khaled
Index for 'khaled':
    https://quotes.toscrape.com/page/10/
    Frequency: 1
    Positions: [111]

>

> find wrld
No pages found
Did you mean: world
> find world
1. https://quotes.toscrape.com/page/9/ (TF-IDF Score: 3.386)
2. https://quotes.toscrape.com/ (TF-IDF Score: 3.386)
3. https://quotes.toscrape.com/page/8/ (TF-IDF Score: 1.693)
4. https://quotes.toscrape.com/page/6/ (TF-IDF Score: 1.693)
5. https://quotes.toscrape.com/page/2/ (TF-IDF Score: 1.693)

>

# Testing

Ensure you are in the root directory for the repository and the virtual environment is activated with pytest installed.

```bash
python -m pytest
```