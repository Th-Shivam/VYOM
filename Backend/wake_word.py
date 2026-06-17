"""
Wake Word Detection Module for VYOM

Provides lightweight wake word filtering while keeping
the existing SpeechRecognition pipeline untouched.

Supported Wake Words:
- Hey Vyom
- Vyom
"""

from config.settings import WAKE_WORD_ENABLED, WAKE_WORDS
from utils.logger import get_logger

logger = get_logger()


class WakeWordManager:

    def __init__(self):
        self.enabled = WAKE_WORD_ENABLED

    def enable(self):
        self.enabled = True
        logger.info("Wake Word Enabled")

    def disable(self):
        self.enabled = False
        logger.info("Wake Word Disabled")

    def process(self, text):

        if not self.enabled:
            return text

        if text is None:
            return None

        text = str(text).strip()

        if text == "":
            return None

        cleaned = text.lower()

        for wake_word in WAKE_WORDS:

            if cleaned.startswith(wake_word):

                logger.info(f"Wake Word Detected : {wake_word}")

                command = text[len(wake_word):].strip()

                if command:
                    return command

                return ""

        logger.info("Wake Word Not Detected")

        return None


wake_manager = WakeWordManager()