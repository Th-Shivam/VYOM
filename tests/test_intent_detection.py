import pytest
from unittest.mock import patch, MagicMock
from Backend.Model import FirstLayerDMM

class TestIntentDetection:
    """Test suite for intent detection functionality in Model.py"""

    @patch('Backend.Model.co.chat_stream')
    def test_general_query(self, mock_chat_stream):
        """Test detection of general conversational queries"""
        # Mock the cohere response
        mock_stream = [
            MagicMock(event_type="text-generation", text="general hello how are you?")
        ]
        mock_chat_stream.return_value = mock_stream

        result = FirstLayerDMM("hello how are you?")
        assert result == ["general hello how are you?"]

    @patch('Backend.Model.co.chat_stream')
    def test_realtime_query(self, mock_chat_stream):
        """Test detection of queries requiring real-time information"""
        mock_stream = [
            MagicMock(event_type="text-generation", text="realtime who is the current president?")
        ]
        mock_chat_stream.return_value = mock_stream

        result = FirstLayerDMM("who is the current president?")
        assert result == ["realtime who is the current president?"]

    @patch('Backend.Model.co.chat_stream')
    def test_open_application(self, mock_chat_stream):
        """Test detection of application opening requests"""
        mock_stream = [
            MagicMock(event_type="text-generation", text="open chrome")
        ]
        mock_chat_stream.return_value = mock_stream

        result = FirstLayerDMM("open chrome")
        assert result == ["open chrome"]

    @patch('Backend.Model.co.chat_stream')
    def test_close_application(self, mock_chat_stream):
        """Test detection of application closing requests"""
        mock_stream = [
            MagicMock(event_type="text-generation", text="close notepad")
        ]
        mock_chat_stream.return_value = mock_stream

        result = FirstLayerDMM("close notepad")
        assert result == ["close notepad"]

    @patch('Backend.Model.co.chat_stream')
    def test_play_song(self, mock_chat_stream):
        """Test detection of music playing requests"""
        mock_stream = [
            MagicMock(event_type="text-generation", text="play let her go")
        ]
        mock_chat_stream.return_value = mock_stream

        result = FirstLayerDMM("play let her go")
        assert result == ["play let her go"]

    @patch('Backend.Model.co.chat_stream')
    def test_generate_image(self, mock_chat_stream):
        """Test detection of image generation requests"""
        mock_stream = [
            MagicMock(event_type="text-generation", text="generate image of a cat")
        ]
        mock_chat_stream.return_value = mock_stream

        result = FirstLayerDMM("generate image of a cat")
        assert result == ["generate image of a cat"]

    @patch('Backend.Model.co.chat_stream')
    def test_set_reminder(self, mock_chat_stream):
        """Test detection of reminder setting requests"""
        mock_stream = [
            MagicMock(event_type="text-generation", text="reminder 9:00pm 25th june business meeting")
        ]
        mock_chat_stream.return_value = mock_stream

        result = FirstLayerDMM("set a reminder at 9:00pm on 25th june for my business meeting")
        assert result == ["reminder 9:00pm 25th june business meeting"]

    @patch('Backend.Model.co.chat_stream')
    def test_system_task(self, mock_chat_stream):
        """Test detection of system control tasks"""
        mock_stream = [
            MagicMock(event_type="text-generation", text="system volume up")
        ]
        mock_chat_stream.return_value = mock_stream

        result = FirstLayerDMM("increase volume")
        assert result == ["system volume up"]

    @patch('Backend.Model.co.chat_stream')
    def test_content_creation(self, mock_chat_stream):
        """Test detection of content creation requests"""
        mock_stream = [
            MagicMock(event_type="text-generation", text="content python tutorial")
        ]
        mock_chat_stream.return_value = mock_stream

        result = FirstLayerDMM("write a python tutorial")
        assert result == ["content python tutorial"]

    @patch('Backend.Model.co.chat_stream')
    def test_google_search(self, mock_chat_stream):
        """Test detection of Google search requests"""
        mock_stream = [
            MagicMock(event_type="text-generation", text="google search machine learning")
        ]
        mock_chat_stream.return_value = mock_stream

        result = FirstLayerDMM("search for machine learning on google")
        assert result == ["google search machine learning"]

    @patch('Backend.Model.co.chat_stream')
    def test_youtube_search(self, mock_chat_stream):
        """Test detection of YouTube search requests"""
        mock_stream = [
            MagicMock(event_type="text-generation", text="youtube search python tutorials")
        ]
        mock_chat_stream.return_value = mock_stream

        result = FirstLayerDMM("search python tutorials on youtube")
        assert result == ["youtube search python tutorials"]

    @patch('Backend.Model.co.chat_stream')
    def test_add_todo(self, mock_chat_stream):
        """Test detection of todo addition requests"""
        mock_stream = [
            MagicMock(event_type="text-generation", text="todo buy groceries")
        ]
        mock_chat_stream.return_value = mock_stream

        result = FirstLayerDMM("add a todo to buy groceries")
        assert result == ["todo buy groceries"]

    @patch('Backend.Model.co.chat_stream')
    def test_list_todos(self, mock_chat_stream):
        """Test detection of todo listing requests"""
        mock_stream = [
            MagicMock(event_type="text-generation", text="list todos")
        ]
        mock_chat_stream.return_value = mock_stream

        result = FirstLayerDMM("show my todos")
        assert result == ["list todos"]

    @patch('Backend.Model.co.chat_stream')
    def test_complete_todo(self, mock_chat_stream):
        """Test detection of todo completion requests"""
        mock_stream = [
            MagicMock(event_type="text-generation", text="complete todo 1")
        ]
        mock_chat_stream.return_value = mock_stream

        result = FirstLayerDMM("mark task 1 as done")
        assert result == ["complete todo 1"]

    @patch('Backend.Model.co.chat_stream')
    def test_delete_todo(self, mock_chat_stream):
        """Test detection of todo deletion requests"""
        mock_stream = [
            MagicMock(event_type="text-generation", text="delete todo 1")
        ]
        mock_chat_stream.return_value = mock_stream

        result = FirstLayerDMM("delete task 1")
        assert result == ["delete todo 1"]

    @patch('Backend.Model.co.chat_stream')
    def test_add_note(self, mock_chat_stream):
        """Test detection of note addition requests"""
        mock_stream = [
            MagicMock(event_type="text-generation", text="note meeting notes: discussed project timeline")
        ]
        mock_chat_stream.return_value = mock_stream

        result = FirstLayerDMM("create a note titled meeting notes with content discussed project timeline")
        assert result == ["note meeting notes: discussed project timeline"]

    @patch('Backend.Model.co.chat_stream')
    def test_list_notes(self, mock_chat_stream):
        """Test detection of note listing requests"""
        mock_stream = [
            MagicMock(event_type="text-generation", text="list notes")
        ]
        mock_chat_stream.return_value = mock_stream

        result = FirstLayerDMM("show my notes")
        assert result == ["list notes"]

    @patch('Backend.Model.co.chat_stream')
    def test_delete_note(self, mock_chat_stream):
        """Test detection of note deletion requests"""
        mock_stream = [
            MagicMock(event_type="text-generation", text="delete note meeting notes")
        ]
        mock_chat_stream.return_value = mock_stream

        result = FirstLayerDMM("delete note meeting notes")
        assert result == ["delete note meeting notes"]

    @patch('Backend.Model.co.chat_stream')
    def test_multiple_tasks(self, mock_chat_stream):
        """Test detection of multiple tasks in a single query"""
        mock_stream = [
            MagicMock(event_type="text-generation", text="open chrome , general who is mahatma gandhi")
        ]
        mock_chat_stream.return_value = mock_stream

        result = FirstLayerDMM("open chrome and tell me about mahatma gandhi")
        assert result == ["open chrome", "general who is mahatma gandhi"]

    @patch('Backend.Model.co.chat_stream')
    def test_exit_command(self, mock_chat_stream):
        """Test detection of exit commands"""
        mock_stream = [
            MagicMock(event_type="text-generation", text="exit")
        ]
        mock_chat_stream.return_value = mock_stream

        result = FirstLayerDMM("bye jarvis")
        assert result == ["exit"]

    @patch('Backend.Model.co.chat_stream')
    def test_invalid_response_filtering(self, mock_chat_stream):
        """Test that invalid responses are filtered out"""
        mock_stream = [
            MagicMock(event_type="text-generation", text="invalid response , general hello")
        ]
        mock_chat_stream.return_value = mock_stream

        result = FirstLayerDMM("hello")
        assert result == ["general hello"]

    @patch('Backend.Model.co.chat_stream')
    def test_recursive_call_on_query_response(self, mock_chat_stream):
        """Test recursive call when response contains '(query)'"""
        # First call returns response with (query)
        first_stream = [
            MagicMock(event_type="text-generation", text="general ( query )")
        ]
        # Second call returns valid response
        second_stream = [
            MagicMock(event_type="text-generation", text="general hello")
        ]
        mock_chat_stream.side_effect = [first_stream, second_stream]

        result = FirstLayerDMM("hello")
        assert result == ["general hello"]
        assert mock_chat_stream.call_count == 2
