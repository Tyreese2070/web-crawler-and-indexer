import pytest
import json
import os
from src.indexer import Indexer
from unittest.mock import patch, mock_open

@pytest.fixture
def indexer():
    return Indexer()

def test_tokenise(indexer):
    text = "I like to eat chicken noodle soup, it's tasty!"
    expected_tokens = ["i", "like", "to", "eat", "chicken", "noodle", "soup", "its", "tasty"]
    tokens = indexer.tokenise(text)
    assert tokens == expected_tokens

def test_build(indexer):
    """Test that the inverted index is built correctly with frequency and positions"""
    pages = [
        {"url": "http://example.com/page1", "text": "I like to eat chicken noodle soup, it's tasty!"},
        {"url": "http://example.com/page2", "text": "Chicken is also tasty."}
    ]

    indexer.build(pages)

    assert "i" in indexer.index
    assert "like" in indexer.index
    assert "chicken" in indexer.index
    assert "noodle" in indexer.index
    assert "soup" in indexer.index
    assert "tasty" in indexer.index
    assert indexer.index["chicken"]["http://example.com/page1"]["frequency"] == 1
    assert indexer.index["chicken"]["http://example.com/page1"]["positions"] == [4]
    assert indexer.index["chicken"]["http://example.com/page2"]["frequency"] == 1
    assert indexer.index["chicken"]["http://example.com/page2"]["positions"] == [0]
    
@patch("os.makedirs")
def test_save_and_load(mock_makedirs, indexer):
    """Test that the index can be saved to and loaded from a JSON file"""
    pages = [
        {"url": "http://example.com/page1", "text": "I like to eat chicken noodle soup, it's tasty!"},
        {"url": "http://example.com/page2", "text": "Chicken is also tasty."}
    ]
    indexer.build(pages)

    # Mock the save process
    with patch("builtins.open", mock_open()) as m:
        indexer.save()
        m.assert_called_once_with(indexer.filepath, "w", encoding="utf-8")

    # Mock the load process
    with patch("builtins.open", mock_open(read_data=json.dumps(indexer.index))) as m:
        new_indexer = Indexer()
        new_indexer.load()
        assert new_indexer.index == indexer.index