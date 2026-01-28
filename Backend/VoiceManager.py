import os
import threading
import time
from enum import Enum
from dotenv import dotenv_values
from utils.logger import get_logger
import pvporcupine
from pvporcupine import create
import pyaudio
import struct

class VoiceMode(Enum):
    WAKE_WORD = "wake_word"
    MANUAL = "manual"
    OFF = "off"

class VoiceManager:
    def __init__(self, initial_mode=None):
        self.logger = get_logger(__name__)
        self.env_vars = dotenv_values(".env")
        self.logger.info(f"Env vars loaded: {self.env_vars}")

        # Configuration - runtime mode overrides env
        env_mode = self.env_vars.get("VOICE_MODE", "wake_word")
        if initial_mode:
            self.mode = VoiceMode(initial_mode)
            self.logger.info(f"Using runtime mode: {initial_mode}")
        else:
            self.mode = VoiceMode(env_mode)
        self.wake_word = self.env_vars.get("WAKE_WORD", "vyom").lower()

        # Components
        self.wake_word_handle = None
        self.audio_stream = None
        self.porcupine = None
        self.audio = None

        # State
        self.is_listening = False
        self.manual_triggered = False

        self.logger.info(f"VoiceManager initialized with mode: {self.mode.value}")

    def start(self):
        """Start the voice manager based on current mode"""
        if self.mode == VoiceMode.WAKE_WORD:
            self._start_wake_word()
        elif self.mode == VoiceMode.MANUAL:
            self._enable_manual_trigger()
        elif self.mode == VoiceMode.OFF:
            self.logger.info("Voice mode is OFF - no listening enabled")

    def stop(self):
        """Stop all voice activities"""
        self.is_listening = False
        self._stop_wake_word()
        self._disable_manual_trigger()

    def activate_once(self):
        """Trigger one-time speech recognition"""
        self.manual_triggered = True
        self.logger.info("Activation triggered")

    def set_mode(self, mode: VoiceMode):
        """Change voice mode dynamically"""
        self.logger.info(f"Changing voice mode from {self.mode.value} to {mode.value}")
        self.stop()
        self.mode = mode
        self.start()

    def _start_wake_word(self):
        """Initialize wake word detection"""
        try:
            # Initialize Porcupine with built-in wake word
            # For custom wake words, you'd need a .ppn file
            self.porcupine = create(
                access_key=os.getenv('PICOVOICE_ACCESS_KEY', ''),  # Will use free tier
                keywords=[self.wake_word] if self.wake_word in ['porcupine', 'bumblebee', 'terminator', 'hey google', 'hey siri', 'alexa', 'ok google', 'computer', 'jarvis'] else ['porcupine']
            )

            self.audio = pyaudio.PyAudio()
            self.audio_stream = self.audio.open(
                rate=self.porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.porcupine.frame_length
            )

            self.is_listening = True
            threading.Thread(target=self._wake_word_loop, daemon=True).start()
            self.logger.info(f"Wake word detection started for: {self.wake_word}")

        except Exception as e:
            self.logger.error(f"Failed to start wake word detection: {e}")
            # Fallback to manual mode
            self.mode = VoiceMode.MANUAL
            self._enable_manual_trigger()

    def _wake_word_loop(self):
        """Main wake word detection loop"""
        while self.is_listening and self.porcupine:
            try:
                pcm = self.audio_stream.read(self.porcupine.frame_length, exception_on_overflow=False)
                pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)

                keyword_index = self.porcupine.process(pcm)
                if keyword_index >= 0:
                    self.logger.info(f"Wake word '{self.wake_word}' detected!")
                    # Wake word detected - trigger ASR
                    self.manual_triggered = True
                    time.sleep(0.5)  # Brief pause to avoid immediate re-trigger

            except Exception as e:
                self.logger.error(f"Error in wake word loop: {e}")
                break

    def _stop_wake_word(self):
        """Stop wake word detection"""
        if self.porcupine:
            self.porcupine.delete()
            self.porcupine = None

        if self.audio_stream:
            self.audio_stream.stop_stream()
            self.audio_stream.close()
            self.audio_stream = None

        if self.audio:
            self.audio.terminate()
            self.audio = None

        self.logger.info("Wake word detection stopped")

    def _enable_manual_trigger(self):
        """Enable manual activation mode"""
        self.logger.info("Manual activation mode enabled")
        # Manual mode is passive - waits for activate_once() calls

    def _disable_manual_trigger(self):
        """Disable manual activation mode"""
        self.manual_triggered = False
        self.logger.info("Manual activation mode disabled")

    def should_listen(self):
        """Check if speech recognition should be triggered"""
        if self.mode == VoiceMode.OFF:
            return False

        if self.mode == VoiceMode.MANUAL:
            if self.manual_triggered:
                self.manual_triggered = False  # Reset trigger
                return True
            return False

        if self.mode == VoiceMode.WAKE_WORD:
            # Wake word mode triggers via wake word detection
            if self.manual_triggered:
                self.manual_triggered = False
                return True
            return False

        return False
