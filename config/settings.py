from pathlib import Path

# Absolute path to project root (VYOM/)
BASE_DIR = Path(__file__).resolve().parent.parent

# Main directories
BACKEND_DIR = BASE_DIR / "Backend"
FRONTEND_DIR = BASE_DIR / "Frontend"
DATA_DIR = BASE_DIR / "Data"

# Frontend sub-directories
FILES_DIR = FRONTEND_DIR / "Files"
GRAPHICS_DIR = FRONTEND_DIR / "Graphics"

fix/add-missing-config-defaults-60
# Chat/logging defaults
CHAT_LOG_PATH = FILES_DIR / "chat_log.json"

# Default LLM model for chatbot
DEFAULT_LLM_MODEL = "llama3-8b-8192"

# Data sub-directories
PRODUCTIVITY_DIR = DATA_DIR / "Productivity"
CHAT_LOG_PATH = DATA_DIR / "chat_log.json"

# LLM Configuration
DEFAULT_LLM_MODEL = "llama-3.3-70b-versatile"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
PRODUCTIVITY_DIR.mkdir(exist_ok=True)
FILES_DIR.mkdir(exist_ok=True)
GRAPHICS_DIR.mkdir(exist_ok=True)
main
