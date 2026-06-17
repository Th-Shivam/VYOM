import os
import sys
from dotenv import dotenv_values

CRITICAL_KEYS = [
    "Username",
    "GroqAPIKey",
]
OPTIONAL_KEYS = [
    "AssistantName",
    "MAX_CONVERSATION_TURNS",
    "MEMORY_INACTIVITY_TIMEOUT",
]
ENV_FILE = ".env"
ENV_TEMPLATE = ".env.example"

RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"


def _banner(colour: str, label: str, message: str) -> None:
    print(f"{colour}{BOLD}[VYOM {label}]{RESET} {message}")


def validate_env_config() -> None:

    if not os.path.isfile(ENV_FILE):
        _banner(RED, "CONFIG ERROR", f"No '{ENV_FILE}' file found in the project root.")
        print(
            f"\n  {CYAN}To fix this:{RESET}\n"
            f"    1. Copy the template:  cp {ENV_TEMPLATE} {ENV_FILE}\n"
            f"    2. Fill in your API keys and username inside '{ENV_FILE}'.\n"
            f"    3. Re-run:  python main.py\n"
        )
        sys.exit(1)

    env_vars = dotenv_values(ENV_FILE)

    missing_critical = [
        key for key in CRITICAL_KEYS
        if not env_vars.get(key, "").strip()
    ]

    if missing_critical:
        _banner(RED, "CONFIG ERROR", "The following required keys are missing or empty in your .env file:\n")
        for key in missing_critical:
            print(f"    {RED}✗  {key}{RESET}")
        print(
            f"\n  {CYAN}To fix this:{RESET}\n"
            f"    Open '{ENV_FILE}' and set the missing values.\n"
            f"    Refer to '{ENV_TEMPLATE}' for the full list of expected keys.\n"
        )
        sys.exit(1)

    missing_optional = [
        key for key in OPTIONAL_KEYS
        if not env_vars.get(key, "").strip()
    ]

    if missing_optional:
        _banner(YELLOW, "CONFIG WARNING", "The following optional keys are not set (defaults will be used):\n")
        for key in missing_optional:
            print(f"    {YELLOW}⚠  {key}{RESET}")
        print()

    _banner(CYAN, "CONFIG OK", "All required environment variables are present. Starting VYOM...\n")