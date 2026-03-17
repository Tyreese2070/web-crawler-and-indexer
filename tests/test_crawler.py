import pytest
from unittest.mock import patch, Mock
from src.crawler import get_page_content

@patch("src.crawler.requests.get")
def test_get_page_content_success(mock_get):
    """
    Test that the get page content function works correctly with a succesful request
    """
    response = Mock()
    response.status_code = 200
    response.text = "<html><body><h1>Chicken Noodle Soup</h1></body></html>"
    mock_get.return_value = response

    result = get_page_content("https://test.com")

    assert result == "<html><body><h1>Chicken Noodle Soup</h1></body></html>"
    mock_get.assert_called_once_with("https://test.com")

@patch("src.crawler.requests.get")
def test_get_page_content_bad(mock_get):
    """
    Test that the get page content function works correctly with a bad request
    """
    response = Mock()
    response.status_code = 404
    mock_get.return_value = response

    result = get_page_content("https://test.com")

    assert result is None

@patch("src.crawler.requests.get")
def test_get_page_content_exception(mock_get):
    """
    Test that the get page content function works correctly with an exception
    """
    mock_get.side_effect = Exception("Network error")

    result = get_page_content("https://test.com")

    assert result is None