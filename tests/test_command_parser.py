import pytest
from unittest.mock import patch, MagicMock
from Backend.Model import FirstLayerDMM

class TestCommandParser:
    """Test cases for command parsing logic in FirstLayerDMM"""

    @patch('Backend.Model.co')
    def test_parse_general_query(self, mock_co):
        """Test parsing of general conversational queries"""
        # Mock the Cohere client response
        mock_stream = MagicMock()
        mock_event = MagicMock()
        mock_event.event_type = "text-generation"
        mock_event.text = "general how are you?"
        mock_stream.__iter__.return_value = [mock_event]
        mock_co.chat_stream.return_value = mock_stream

        result = FirstLayerDMM("how are you?")

        assert "general how are you?" in result

    @patch('Backend.Model.co')
    def test_parse_realtime_query(self, mock_co):
        """Test parsing of realtime queries requiring up-to-date information"""
        mock_stream = MagicMock()
        mock_event = MagicMock()
        mock_event.event_type = "text-generation"
        mock_event.text = "realtime who is the current president?"
        mock_stream.__iter__.return_value = [mock_event]
        mock_co.chat_stream.return_value = mock_stream

        result = FirstLayerDMM("who is the current president?")

        assert "realtime who is the current president?" in result

    @patch('Backend.Model.co')
    def test_parse_open_application(self, mock_co):
        """Test parsing of application opening commands"""
        mock_stream = MagicMock()
        mock_event = MagicMock()
        mock_event.event_type = "text-generation"
        mock_event.text = "open chrome"
        mock_stream.__iter__.return_value = [mock_event]
        mock_co.chat_stream.return_value = mock_stream

        result = FirstLayerDMM("open chrome")

        assert "open chrome" in result

    @patch('Backend.Model.co')
    def test_parse_multiple_commands(self, mock_co):
        """Test parsing of multiple commands in a single query"""
        mock_stream = MagicMock()
        mock_event = MagicMock()
        mock_event.event_type = "text-generation"
        mock_event.text = "open chrome , open firefox"
        mock_stream.__iter__.return_value = [mock_event]
        mock_co.chat_stream.return_value = mock_stream

        result = FirstLayerDMM("open chrome and firefox")

        assert "open chrome" in result
        assert "open firefox" in result

    @patch('Backend.Model.co')
    def test_parse_todo_command(self, mock_co):
        """Test parsing of todo creation commands"""
        mock_stream = MagicMock()
        mock_event = MagicMock()
        mock_event.event_type = "text-generation"
        mock_event.text = "todo buy groceries"
        mock_stream.__iter__.return_value = [mock_event]
        mock_co.chat_stream.return_value = mock_stream

        result = FirstLayerDMM("add a todo to buy groceries")

        assert "todo buy groceries" in result

    @patch('Backend.Model.co')
    def test_parse_exit_command(self, mock_co):
        """Test parsing of exit commands"""
        mock_stream = MagicMock()
        mock_event = MagicMock()
        mock_event.event_type = "text-generation"
        mock_event.text = "exit"
        mock_stream.__iter__.return_value = [mock_event]
        mock_co.chat_stream.return_value = mock_stream

        result = FirstLayerDMM("bye")

        assert "exit" in result

    @patch('Backend.Model.co')
    def test_empty_input(self, mock_co):
        """Test handling of empty input"""
        mock_stream = MagicMock()
        mock_event = MagicMock()
        mock_event.event_type = "text-generation"
        mock_event.text = "general"
        mock_stream.__iter__.return_value = [mock_event]
        mock_co.chat_stream.return_value = mock_stream

        result = FirstLayerDMM("")

        assert isinstance(result, list)

    @patch('Backend.Model.co')
    def test_invalid_command_fallback(self, mock_co):
        """Test fallback to general query for unrecognized commands"""
        mock_stream = MagicMock()
        mock_event = MagicMock()
        mock_event.event_type = "text-generation"
        mock_event.text = "general unrecognized command"
        mock_stream.__iter__.return_value = [mock_event]
        mock_co.chat_stream.return_value = mock_stream

        result = FirstLayerDMM("some random command")

        assert "general unrecognized command" in result
