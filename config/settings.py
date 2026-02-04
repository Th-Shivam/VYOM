from pathlib import Path

# Absolute path to project root (VYOM/)
BASE_DIR = Path(__file__).resolve().parent.parent

# Main directories
BACKEND_DIR = BASE_DIR / "Backend"
FRONTEND_DIR = BASE_DIR / "Frontend"

# Frontend sub-directories
FILES_DIR = FRONTEND_DIR / "Files"
GRAPHICS_DIR = FRONTEND_DIR / "Graphics"

# Chat/logging defaults
CHAT_LOG_PATH = FILES_DIR / "chat_log.json"

# Default LLM model for chatbot
DEFAULT_LLM_MODEL = "llama3-8b-8192"
