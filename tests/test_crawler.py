import pytest
from unittest.mock import patch, Mock
from src.crawler import get_page_content, crawl

# ========= get_page_content tests ===========

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

# ========= crawl tests ===========
@patch("src.crawler.time.sleep")
@patch("src.crawler.get_page_content")
def test_crawl(mock_get_page_content, mock_sleep):
    """
    Test that the crawl function works correctly with a simple page structure
    """

    # Page with next button
    page_1 = """
    <html>
        <body>
            <h1>Page 1</h1>
            <li class="next"><a href="/page/2">Next</a></li>
        </body>
    </html>
    """

    # Page without next button
    page_2 = """
    <html>
        <body>
            <h1>Page 2</h1>
        </body>
    </html>
    """

    mock_get_page_content.side_effect = [page_1, page_2]
    result = crawl("https://test.com")

    assert len(result) == 2
    assert result[0]["url"] == "https://test.com"
    assert result[0]["text"] == "Page 1 Next"
    assert result[1]["url"] == "https://test.com/page/2"
    assert result[1]["text"] == "Page 2"
    mock_sleep.assert_called_with(6)

@patch("src.crawler.time.sleep")
@patch("src.crawler.get_page_content")
def test_crawl_infinite_loop(mock_get_page_content, mock_sleep):
    """
    Test that the crawl function doesn't get stuck in a loop
    """

    page_1 = """
    <html>
        <body>
            <h1>Page 1</h1>
            <li class="next"><a href="/page/2">Next</a></li>
        </body>
    </html>
    """

    page_2 = """
    <html>
        <body>
            <h1>Page 2</h1>
            <li class="next"> <a href="/page/1">Next</a></li>
        </body>
    </html>
    """
    mock_get_page_content.side_effect = [page_1, page_2, page_1, page_2]
    result = crawl("https://test.com/page/1")

    assert len(result) == 2
    assert result[0]["url"] == "https://test.com/page/1"
    assert result[1]["url"] == "https://test.com/page/2"

