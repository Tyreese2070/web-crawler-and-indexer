# web-crawler-and-indexer
![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)
[![Build Status](https://github.com/tyreese2070/web-crawler-and-indexer/actions/workflows/tests.yml/badge.svg)](https://github.com/tyreese2070/web-crawler-and-indexer/actions/workflows/tests.yml)
![Coverage](./coverage.svg)

# Overview
A command line web crawler, indexer, and search engine. The tool recursively crawls https://quotes.toscrape.com/ with a 6 second politeness window, and parses the HTML content to build an inverted index. 

This also includes some additional features such as intersections, TF-IDF ranking, and query suggestions

# Installation and Setup
**Requires Python 3.12 or higher.**

**Developed using Python 3.14.3**

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

## Commands

Build: Crawls https://quotes.toscrape.com/ with a 6 second politeness window and builds the index. This takes around two minutes.

Load: Loads the index into memory. This requires the build command to be run if index.json isn't in /data.

Print: Displays the URLs the word can be found on as well as its frequency and position on that page.

Find: Finds all occurrences of the given input and sorts their appearances by TF-IDF score.

Help: Displays the avaiable commands to use.

Exit: Exits the command line interface.

## Example CLI Session:

```text
Commands: build, load, print <word>, find <query>, help, exit

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
```
# Testing
![Coverage](./coverage.svg)

The tests produced are unit tests that cover the core features of the crawler and search engine. Each source file has its own associated testing file. 

Whenever code is pushed to the repository, these tests are run to ensure that new changes didn't break any existing features.

```bash
python -m pytest
```

# Directory Structure
```text
├───.github
│   └───workflows           # Configuration for automated testing
|
├───data
│   └───index.json          # Compiled index file produced by the build command
|
├───src
│   └───main.py             # Main file for the Command Line Interface
│   └───crawler.py          # Contains implementation of the web crawler
│   └───indexer.py          # Contains the implementation index building and saving
│   └───search.py           # Contains the implementation of the print and search featues
|
├───tests                   # Contains the unit tests for each source file
│   └───test_main.py
│   └───test_crawler.py
│   └───test_indexer.py
│   └───test_search.py
```