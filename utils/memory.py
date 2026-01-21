import os
import datetime
from dotenv import dotenv_values
from utils.logger import get_logger

# Load environment variables
env_vars = dotenv_values(".env")

# Get memory configuration with defaults
MAX_CONVERSATION_TURNS = int(env_vars.get("MAX_CONVERSATION_TURNS", 10))
MEMORY_INACTIVITY_TIMEOUT = int(env_vars.get("MEMORY_INACTIVITY_TIMEOUT", 300))  # seconds

class MemoryManager:
    def __init__(self):
        self.memory = []
        self.last_activity = datetime.datetime.now()
        self.logger = get_logger(__name__)
        # Load env vars from environment or .env file
        self.MAX_CONVERSATION_TURNS = int(os.getenv("MAX_CONVERSATION_TURNS", 10))
        self.MEMORY_INACTIVITY_TIMEOUT = int(os.getenv("MEMORY_INACTIVITY_TIMEOUT", 300))

    def add_message(self, role: str, content: str):
        """Add a new message to memory and trim if necessary."""
        timestamp = datetime.datetime.now()
        self.memory.append({
            "role": role,
            "content": content,
            "timestamp": timestamp.isoformat()
        })
        self.last_activity = timestamp
        self.trim_memory()
        self.logger.debug(f"Added {role} message. Memory size: {len(self.memory)}")

    def get_context(self):
        """Get the current conversation context."""
        return self.memory.copy()

    def trim_memory(self):
        """Trim memory to keep only the last MAX_CONVERSATION_TURNS * 2 messages."""
        max_messages = self.MAX_CONVERSATION_TURNS * 2
        if len(self.memory) > max_messages:
            trimmed_count = len(self.memory) - max_messages
            self.memory = self.memory[-max_messages:]
            self.logger.info(f"Memory trimmed by {trimmed_count} messages. Current size: {len(self.memory)}")

    def cleanup_if_inactive(self):
        """Clear memory if inactive for more than MEMORY_INACTIVITY_TIMEOUT seconds."""
        now = datetime.datetime.now()
        if (now - self.last_activity).total_seconds() > self.MEMORY_INACTIVITY_TIMEOUT:
            self.memory.clear()
            self.logger.info("Conversation memory cleared due to inactivity")

    def load_from_file(self, file_path: str):
        """Load memory from a JSON file."""
        try:
            import json
            with open(file_path, "r") as f:
                data = json.load(f)
                # Convert timestamp strings back to datetime objects
                for msg in data:
                    if "timestamp" in msg:
                        msg["timestamp"] = datetime.datetime.fromisoformat(msg["timestamp"])
                self.memory = data
                if self.memory:
                    self.last_activity = self.memory[-1]["timestamp"]
                self.logger.info(f"Loaded {len(self.memory)} messages from {file_path}")
        except FileNotFoundError:
            self.logger.info(f"No existing memory file found at {file_path}")
        except Exception as e:
            self.logger.error(f"Error loading memory from {file_path}: {e}")

    def save_to_file(self, file_path: str):
        """Save memory to a JSON file."""
        try:
            import json
            # Remove timestamp for JSON serialization to avoid datetime issues
            data = []
            for msg in self.memory:
                msg_copy = msg.copy()
                msg_copy.pop("timestamp", None)
                data.append(msg_copy)

            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)
            self.logger.debug(f"Saved {len(self.memory)} messages to {file_path}")
        except Exception as e:
            self.logger.error(f"Error saving memory to {file_path}: {e}")
