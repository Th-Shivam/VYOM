from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
LOG_DIR = DATA_DIR / "logs"

CHAT_LOG_PATH = DATA_DIR / "ChatLog.json"
USER_CONFIG_PATH = DATA_DIR / "user_config.json"
DEFAULT_LLM_MODEL = "llama-3.3-70b-versatile"
