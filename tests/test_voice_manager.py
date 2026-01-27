import pytest
from unittest.mock import patch, MagicMock, mock_open
from Backend.VoiceManager import VoiceManager, VoiceMode

class TestVoiceManager:
    """Test cases for VoiceManager functionality"""

    @patch('Backend.VoiceManager.dotenv_values')
    def test_init_default_mode(self, mock_dotenv):
        """Test VoiceManager initialization with default wake_word mode"""
        mock_dotenv.return_value = {'VOICE_MODE': 'wake_word', 'WAKE_WORD': 'vyom'}

        vm = VoiceManager()
        assert vm.mode == VoiceMode.WAKE_WORD
        assert vm.wake_word == 'vyom'

    @patch('Backend.VoiceManager.dotenv_values')
    def test_init_runtime_mode_override(self, mock_dotenv):
        """Test VoiceManager initialization with runtime mode override"""
        mock_dotenv.return_value = {'VOICE_MODE': 'wake_word', 'WAKE_WORD': 'vyom'}

        vm = VoiceManager(initial_mode='manual')
        assert vm.mode == VoiceMode.MANUAL
        assert vm.wake_word == 'vyom'

    @patch('Backend.VoiceManager.dotenv_values')
    def test_init_off_mode(self, mock_dotenv):
        """Test VoiceManager initialization with off mode"""
        mock_dotenv.return_value = {'VOICE_MODE': 'off', 'WAKE_WORD': 'vyom'}

        vm = VoiceManager()
        assert vm.mode == VoiceMode.OFF

    @patch('Backend.VoiceManager.dotenv_values')
    @patch('Backend.VoiceManager.os.getenv')
    def test_start_wake_word_mode(self, mock_getenv, mock_dotenv):
        """Test starting wake word mode"""
        mock_dotenv.return_value = {'VOICE_MODE': 'wake_word', 'WAKE_WORD': 'vyom'}
        mock_getenv.return_value = 'test_access_key'  # Mock access key

        with patch('Backend.VoiceManager.create') as mock_create, \
             patch('Backend.VoiceManager.pyaudio.PyAudio') as mock_pyaudio, \
             patch('Backend.VoiceManager.threading.Thread') as mock_thread:

            mock_porcupine_instance = MagicMock()
            mock_porcupine_instance.sample_rate = 16000
            mock_porcupine_instance.frame_length = 512
            mock_create.return_value = mock_porcupine_instance

            mock_audio = MagicMock()
            mock_pyaudio.return_value = mock_audio
            mock_stream = MagicMock()
            mock_audio.open.return_value = mock_stream

            vm = VoiceManager()
            vm.start()

            assert vm.is_listening == True
            mock_create.assert_called_once()
            mock_pyaudio.assert_called_once()
            mock_thread.assert_called_once()

    @patch('Backend.VoiceManager.dotenv_values')
    def test_start_manual_mode(self, mock_dotenv):
        """Test starting manual mode"""
        mock_dotenv.return_value = {'VOICE_MODE': 'manual', 'WAKE_WORD': 'vyom'}

        vm = VoiceManager()
        vm.start()

        assert vm.is_listening == False
        assert vm.manual_triggered == False

    @patch('Backend.VoiceManager.dotenv_values')
    def test_start_off_mode(self, mock_dotenv):
        """Test starting off mode"""
        mock_dotenv.return_value = {'VOICE_MODE': 'off', 'WAKE_WORD': 'vyom'}

        vm = VoiceManager()
        vm.start()

        assert vm.is_listening == False

    @patch('Backend.VoiceManager.dotenv_values')
    def test_activate_once_manual_mode(self, mock_dotenv):
        """Test manual activation in manual mode"""
        mock_dotenv.return_value = {'VOICE_MODE': 'manual', 'WAKE_WORD': 'vyom'}

        vm = VoiceManager()
        vm.activate_once()

        assert vm.manual_triggered == True

    @patch('Backend.VoiceManager.dotenv_values')
    def test_should_listen_off_mode(self, mock_dotenv):
        """Test should_listen returns False in off mode"""
        mock_dotenv.return_value = {'VOICE_MODE': 'off', 'WAKE_WORD': 'vyom'}

        vm = VoiceManager()
        assert vm.should_listen() == False

    @patch('Backend.VoiceManager.dotenv_values')
    def test_should_listen_manual_mode_not_triggered(self, mock_dotenv):
        """Test should_listen returns False in manual mode when not triggered"""
        mock_dotenv.return_value = {'VOICE_MODE': 'manual', 'WAKE_WORD': 'vyom'}

        vm = VoiceManager()
        assert vm.should_listen() == False

    @patch('Backend.VoiceManager.dotenv_values')
    def test_should_listen_manual_mode_triggered(self, mock_dotenv):
        """Test should_listen returns True in manual mode when triggered"""
        mock_dotenv.return_value = {'VOICE_MODE': 'manual', 'WAKE_WORD': 'vyom'}

        vm = VoiceManager()
        vm.activate_once()
        assert vm.should_listen() == True
        # Should reset trigger after should_listen
        assert vm.manual_triggered == False

    @patch('Backend.VoiceManager.dotenv_values')
    def test_should_listen_wake_word_mode_not_triggered(self, mock_dotenv):
        """Test should_listen returns False in wake word mode when not triggered"""
        mock_dotenv.return_value = {'VOICE_MODE': 'wake_word', 'WAKE_WORD': 'vyom'}

        vm = VoiceManager()
        assert vm.should_listen() == False

    @patch('Backend.VoiceManager.dotenv_values')
    @patch('Backend.VoiceManager.os.getenv')
    def test_should_listen_wake_word_mode_triggered(self, mock_getenv, mock_dotenv):
        """Test should_listen returns True in wake word mode when triggered"""
        mock_dotenv.return_value = {'VOICE_MODE': 'wake_word', 'WAKE_WORD': 'vyom'}
        mock_getenv.return_value = 'test_access_key'  # Mock access key

        vm = VoiceManager()
        vm.activate_once()  # Simulate wake word detection
        assert vm.should_listen() == True
        # Should reset trigger after should_listen
        assert vm.manual_triggered == False

    @patch('Backend.VoiceManager.dotenv_values')
    def test_set_mode(self, mock_dotenv):
        """Test dynamic mode switching"""
        mock_dotenv.return_value = {'VOICE_MODE': 'wake_word', 'WAKE_WORD': 'vyom'}

        vm = VoiceManager()
        vm.set_mode(VoiceMode.MANUAL)

        assert vm.mode == VoiceMode.MANUAL

    @patch('Backend.VoiceManager.dotenv_values')
    @patch('Backend.VoiceManager.os.getenv')
    def test_stop_wake_word_mode(self, mock_getenv, mock_dotenv):
        """Test stopping wake word mode"""
        mock_dotenv.return_value = {'VOICE_MODE': 'wake_word', 'WAKE_WORD': 'vyom'}
        mock_getenv.return_value = 'test_access_key'  # Mock access key

        with patch('Backend.VoiceManager.create') as mock_create, \
             patch('Backend.VoiceManager.pyaudio.PyAudio') as mock_pyaudio:

            mock_porcupine_instance = MagicMock()
            mock_porcupine_instance.sample_rate = 16000
            mock_porcupine_instance.frame_length = 512
            mock_create.return_value = mock_porcupine_instance

            mock_audio = MagicMock()
            mock_pyaudio.return_value = mock_audio
            mock_stream = MagicMock()
            mock_audio.open.return_value = mock_stream

            vm = VoiceManager()
            vm.start()
            vm.stop()

            assert vm.is_listening == False
            mock_porcupine_instance.delete.assert_called_once()
            mock_stream.stop_stream.assert_called_once()
            mock_stream.close.assert_called_once()
            mock_audio.terminate.assert_called_once()
