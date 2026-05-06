import pytest
from src.indexer import Indexer
from src.search import print_word, find_query

@pytest.fixture
def mock_indexer():
    """
    Creates a mock indexer with a preset index for testing.
    """
    indexer = Indexer()
    indexer.index = {
        "hello": {"http://hello.com/page1": {"frequency": 5, "positions": [0]}},
        "world": {"http://world.com/page2": {"frequency": 3, "positions": [1]},
                  "http://test.com/page3": {"frequency": 1, "positions": [0]}
                  },
        "test": {"http://test.com/page3": {"frequency": 2, "positions": [2, 3]}}
    }
    return indexer

def test_print_word_found(capsys, mock_indexer):
    """
    Test that print_word correctly prints the word and its associated URLs
    and frequencies when the word is found in the index.
    """
    print_word(mock_indexer, "hello")
    captured = capsys.readouterr()
    assert "hello" in captured.out
    assert "http://hello.com/page1" in captured.out
    assert "Frequency: 5" in captured.out

def test_print_word_not_found(capsys, mock_indexer):
    """
    Test that print_word correctly indicates when a word is not found in the index.
    """
    print_word(mock_indexer, "wookie")
    captured = capsys.readouterr()
    assert "not found in index" in captured.out

def test_find_tf_idf_ranking(capsys, mock_indexer):
    """
    Test that find_query correctly ranks URLs based on TF-IDF scores for a single word query.
    """
    find_query(mock_indexer, "world")
    captured = capsys.readouterr()
    assert captured.out.index("http://world.com/page2") < captured.out.index("http://test.com/page3")

def test_find_query_intersection(capsys, mock_indexer):
    """
    Test that find_query correctly finds the intersection of URLs for multiple word queries.
    """
    find_query(mock_indexer, "world test")
    captured = capsys.readouterr()
    assert "http://test.com/page3" in captured.out
    assert "http://world.com/page2" not in captured.out

def test_find_query_spellcheck(capsys, mock_indexer):
    """
    Test that find_query correctly suggests spelling corrections for misspelled words.
    """
    find_query(mock_indexer, "worl")
    captured = capsys.readouterr()
    assert "Did you mean: world" in captured.out

def test_find_query_no_intersection(capsys, mock_indexer):
    """
    Test that find_query correctly indicates when no URLs match all queried words.
    """
    find_query(mock_indexer, "hello test")
    captured = capsys.readouterr()
    assert "No pages found" in captured.out