import pytest
from unittest.mock import patch, MagicMock
from Backend.ChatBot import ChatBot, AnswerModifier

class TestResponseFormatter:
    """Test cases for response formatting and chatbot logic"""

    def test_answer_modifier_removes_empty_lines(self):
        """Test that AnswerModifier removes empty lines"""
        input_text = "Line 1\n\n\nLine 2\n\nLine 3"
        result = AnswerModifier(input_text)

        expected = "Line 1\nLine 2\nLine 3"
        assert result == expected

    def test_answer_modifier_preserves_content(self):
        """Test that AnswerModifier preserves actual content"""
        input_text = "Hello\n\nWorld\n\nTest"
        result = AnswerModifier(input_text)

        assert "Hello" in result
        assert "World" in result
        assert "Test" in result
        assert "\n\n" not in result

    def test_answer_modifier_single_line(self):
        """Test AnswerModifier with single line input"""
        input_text = "Single line response"
        result = AnswerModifier(input_text)

        assert result == "Single line response"

    def test_answer_modifier_all_empty_lines(self):
        """Test AnswerModifier with all empty lines"""
        input_text = "\n\n\n"
        result = AnswerModifier(input_text)

        assert result == ""

    @patch('Backend.ChatBot.client')
    @patch('Backend.ChatBot.memory_manager')
    def test_chatbot_successful_response(self, mock_memory, mock_client):
        """Test successful chatbot response generation"""
        # Mock memory manager
        mock_memory.cleanup_if_inactive.return_value = None
        mock_memory.get_context.return_value = []
        mock_memory.add_message.return_value = None
        mock_memory.save_to_file.return_value = None

        # Mock Groq client response
        mock_completion = MagicMock()
        mock_chunk = MagicMock()
        mock_chunk.choices = [MagicMock()]
        mock_chunk.choices[0].delta.content = "Hello, how can I help?"
        mock_completion.__iter__.return_value = [mock_chunk]
        mock_client.chat.completions.create.return_value = mock_completion

        result = ChatBot("Hello")

        assert "Hello, how can I help?" in result
        mock_memory.add_message.assert_called()
        mock_memory.save_to_file.assert_called()

    @patch('Backend.ChatBot.client')
    @patch('Backend.ChatBot.memory_manager')
    def test_chatbot_handles_exception(self, mock_memory, mock_client):
        """Test chatbot error handling"""
        # Mock memory manager
        mock_memory.cleanup_if_inactive.return_value = None
        mock_memory.memory.clear.return_value = None
        mock_memory.save_to_file.return_value = None

        # Mock client to raise exception
        mock_client.chat.completions.create.side_effect = Exception("API Error")

        # Mock recursive call to succeed
        with patch('Backend.ChatBot.ChatBot', return_value="Recovered response"):
            result = ChatBot("Test query")

        assert "Recovered response" in result
        mock_memory.memory.clear.assert_called()

    @patch('Backend.ChatBot.datetime')
    def test_real_time_information_format(self, mock_datetime):
        """Test real-time information formatting"""
        from Backend.ChatBot import RealTimeInformation

        # Mock datetime
        mock_now = MagicMock()
        mock_now.strftime.side_effect = lambda fmt: {
            "%A": "Monday",
            "%d": "15",
            "%B": "January",
            "%Y": "2024",
            "%H": "14",
            "%M": "30",
            "%S": "45"
        }[fmt]
        mock_datetime.datetime.now.return_value = mock_now

        result = RealTimeInformation()

        assert "Monday" in result
        assert "15" in result
        assert "January" in result
        assert "2024" in result
        assert "14" in result
        assert "30" in result
        assert "45" in result

    @patch('Backend.ChatBot.client')
    @patch('Backend.ChatBot.memory_manager')
    def test_chatbot_memory_cleanup_on_inactive(self, mock_memory, mock_client):
        """Test memory cleanup when inactive"""
        mock_memory.cleanup_if_inactive.return_value = True  # Simulate cleanup needed
        mock_memory.get_context.return_value = []
        mock_memory.add_message.return_value = None
        mock_memory.save_to_file.return_value = None

        # Mock successful response
        mock_completion = MagicMock()
        mock_chunk = MagicMock()
        mock_chunk.choices = [MagicMock()]
        mock_chunk.choices[0].delta.content = "Response"
        mock_completion.__iter__.return_value = [mock_chunk]
        mock_client.chat.completions.create.return_value = mock_completion

        ChatBot("Test")

        mock_memory.cleanup_if_inactive.assert_called_once()

    @patch('Backend.ChatBot.client')
    @patch('Backend.ChatBot.memory_manager')
    def test_chatbot_response_modification(self, mock_memory, mock_client):
        """Test that responses are properly modified"""
        mock_memory.cleanup_if_inactive.return_value = None
        mock_memory.get_context.return_value = []
        mock_memory.add_message.return_value = None
        mock_memory.save_to_file.return_value = None

        # Mock response with extra content that should be cleaned
        mock_completion = MagicMock()
        mock_chunk = MagicMock()
        mock_chunk.choices = [MagicMock()]
        mock_chunk.choices[0].delta.content = "Response\n\nwith\n\n\nextra\nlines</s>"
        mock_completion.__iter__.return_value = [mock_chunk]
        mock_client.chat.completions.create.return_value = mock_completion

        result = ChatBot("Test")

        # Should not contain </s> or extra empty lines
        assert "</s>" not in result
        assert "\n\n\n" not in result
