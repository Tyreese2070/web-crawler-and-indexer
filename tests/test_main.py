import pytest
from unittest.mock import patch
from src.main import main

@patch("builtins.input", side_effect=["exit"])
def test_main_exit(mock_input, capsys):
    """
    Test that the main function exits when the user types 'exit'.
    """
    main()
    captured = capsys.readouterr()
    assert "Exiting" in captured.out

@patch("builtins.input", side_effect=[EOFError])
def test_main_eof(mock_input, capsys):
    """
    Test that the main function exits when an EOFError is raised.
    """
    main()
    captured = capsys.readouterr()
    assert "Exiting" in captured.out

@patch("builtins.input", side_effect=["invalid_command", "exit"])
def test_main_unknown_command(mock_input, capsys):
    """
    Test that the main function handles unknown commands.
    """
    with patch("builtins.input", side_effect=["unknown", "exit"]):
        main()
        captured = capsys.readouterr()
        assert "Unknown command" in captured.out

@patch("builtins.input", side_effect=["build", "exit"])
@patch("src.main.crawl")
@patch("src.indexer.Indexer.save")
def test_main_build_success(mock_save, mock_crawl, mock_input, capsys):
    """
    Test that the build command calls the crawler and saves the index.
    """
    mock_crawl.return_value = [{"url": "http://test.com", "text": "hello"}]

    main()
    captured = capsys.readouterr()
    mock_crawl.assert_called_once()
    mock_save.assert_called_once()
    assert "Built and saved index" in captured.out

@patch("builtins.input", side_effect=["load", "exit"])
@patch("src.indexer.Indexer.load")
def test_main_load(mock_load, mock_input, capsys):
    """
    Test that the load command correctly triggers the indexer's load method.
    """
    main()
    mock_load.assert_called_once()

@patch("builtins.input", side_effect=["print hello", "exit"])
def test_main_print_not_loaded(mock_input, capsys):
    """
    Test that printing cannot happpen before loading or building the index.
    """
    main()
    captured = capsys.readouterr()
    assert "Failed to load index, run build or load first" in captured.out

@patch("builtins.input", side_effect=["find hello", "exit"])
def test_main_find_not_loaded(mock_input, capsys):
    """
    Test that searching cannot happen before loading or building the index.
    """
    main()
    captured = capsys.readouterr()
    assert "Failed to load index, run build or load first" in captured.out

@patch("builtins.input", side_effect=["print hello", "find world", "exit"])
@patch("src.main.print_word")
@patch("src.main.find_query")
def test_main_commands_when_loaded(mock_find, mock_print, mock_input, capsys):
    """
    Test that print and find commands correctly route to search.py when the index is ready.
    """
    with patch("src.main.Indexer") as MockIndexer:
        mock_instance = MockIndexer.return_value
        mock_instance.index = {"chicken": "soup"}
        main()
        mock_print.assert_called_once_with(mock_instance, "hello")
        mock_find.assert_called_once_with(mock_instance, "world")