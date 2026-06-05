import cohere
from rich import print
from dotenv import dotenv_values
from utils.logger import get_logger

env_vars = dotenv_values(".env")

CohereAPIKey = env_vars.get("CohereAPIKey")

co = cohere.Client(api_key=CohereAPIKey)

logger = get_logger()

# List of functions/intents recognized by the model
funcs = [
    "exit", "general", "realtime", "open", "close", "play", "generate image",
    "system", "content", "google search", "youtube search", "reminder",
    "todo", "note", "list todos", "list notes", "complete todo",
    "delete note", "delete todo"
]

# Define the preamble that guides the model on how to categorize queries
preamble = """
You are a Decision-Making Model for a voice assistant. Your ONLY job is to classify user queries into specific categories. You must respond with EXACTLY one category and the query content in parentheses.

CRITICAL: Do not explain, do not add extra text, just respond with the exact format shown.

CATEGORIES:
- 'general (query)' - For conversational queries, questions, or anything that doesn't fit other categories
- 'realtime (query)' - For queries needing current information like news, weather, current events
- 'open (app/website)' - For opening applications or websites (e.g., 'open chrome', 'open facebook')
- 'close (app)' - For closing applications (e.g., 'close notepad')
- 'play (song)' - For playing music (e.g., 'play music', 'play let her go')
- 'generate image (prompt)' - For image generation requests
- 'system (task)' - For system controls like volume, brightness
- 'content (topic)' - For content creation requests
- 'google search (topic)' - For Google searches
- 'youtube search (topic)' - For YouTube searches
- 'todo (task)' - For adding todo items
- 'list todos' - For listing todos
- 'complete todo (id)' - For completing todos
- 'delete todo (id)' - For deleting todos
- 'note (title: content)' - For creating notes
- 'list notes' - For listing notes
- 'delete note (title)' - For deleting notes
- 'reminder (time details)' - For setting reminders
- 'exit' - For ending the conversation

EXAMPLES:
User: "open chrome"
Response: open chrome

User: "what is the weather"
Response: realtime what is the weather

User: "hello"
Response: general hello

User: "add a todo to buy groceries"
Response: todo buy groceries

User: "play music"
Response: play music

User: "remind me about the meeting at 5pm"
Response: reminder 5pm meeting

Respond with ONLY the category and content, nothing else.
"""

# Define a chat history with predefined user-chatbot interactions for context
ChatHistory = [
    {"role": "USER", "message": "how are you ?"},
    {"role": "CHATBOT", "message": "general how are you ?"},
    {"role": "USER", "message": "do you like pizza ?"},
    {"role": "CHATBOT", "message": "general do you like pizza ?"},
    {"role": "USER", "message": "open chrome and tell me about mahatma gandhi"},
    {"role": "CHATBOT", "message": "open chrome , general who is mahatma gandhi"},
    {"role": "USER", "message": "open chrome and firefox"},
    {"role": "CHATBOT", "message": "open chrome , open firefox"},
    {"role": "USER", "message": "what is today's date and remind me that i have a dancing performance on 5th august 11:00 pm"},
    {"role": "CHATBOT", "message": "general what is today's date , reminder 11:00 pm 5th august dancing performance"},
    {"role": "USER", "message": "chat with me"},
    {"role": "CHATBOT", "message": "general chat with me"},
]


def rule_based_intent_detection(prompt: str):
    """Simple rule-based intent detection as fallback when API fails."""
    prompt_lower = prompt.lower().strip()

    if any(word in prompt_lower for word in ["bye", "exit", "quit", "goodbye", "see you"]):
        return "exit", 0.9

    if prompt_lower.startswith("open "):
        return f"open {prompt_lower[5:].strip()}", 0.8

    if prompt_lower.startswith("close "):
        return f"close {prompt_lower[6:].strip()}", 0.8

    if prompt_lower.startswith("play "):
        return f"play {prompt_lower[5:].strip()}", 0.8

    if "generate image" in prompt_lower or "create image" in prompt_lower:
        return f"generate image {prompt}", 0.7

    if "add a todo" in prompt_lower or "add todo" in prompt_lower:
        task = prompt_lower.replace("add a todo", "").replace("add todo", "").strip()
        return f"todo {task}", 0.8

    if "list todos" in prompt_lower or "show my todos" in prompt_lower:
        return "list todos", 0.9

    if "list notes" in prompt_lower or "show my notes" in prompt_lower:
        return "list notes", 0.9

    if any(word in prompt_lower for word in ["remind", "reminder"]):
        return f"reminder {prompt}", 0.8

    if any(word in prompt_lower for word in ["news", "today", "current", "latest"]):
        return f"realtime {prompt}", 0.6

    return f"general {prompt}", 0.8


def calculate_response_confidence(response: str, prompt: str) -> float:
    """Calculate confidence score based on response quality and prompt matching."""
    response_lower = response.lower().strip()
    prompt_lower = prompt.lower().strip()

    # High confidence if response starts with a recognized multi-word or single-word func
    matched_func = next((f for f in sorted(funcs, key=len, reverse=True)
                         if response_lower.startswith(f)), None)
    if matched_func:
        prompt_words = set(prompt_lower.split())
        response_words = set(response_lower.split())
        if prompt_words & response_words:
            return 0.9
        return 0.8

    if any(f in response_lower for f in funcs):
        return 0.7

    if len(response.split()) < 3:
        return 0.5

    return 0.6


def parse_intent(task: str, funcs: list) -> str | None:
    """
    Match a task string against known multi-word and single-word function names.
    Returns the matched intent string or None if no match found.
    """
    task_lower = task.lower().strip()
    # Check multi-word funcs first (longest match wins)
    for func in sorted(funcs, key=len, reverse=True):
        if task_lower.startswith(func):
            return task  # Return original case
    return None


def FirstLayerDMM(prompt: str = "test"):
    """Classify a user prompt into one or more intent categories."""

    # Try Cohere API first, fallback to rule-based if it fails
    try:
        response_obj = co.chat(
            model="command-r-08-2024",
            message=prompt,
            preamble=preamble,          # FIX: pass preamble correctly
            chat_history=ChatHistory,   # FIX: use properly formatted ChatHistory
            max_tokens=100,
            temperature=0.1,            # FIX: low temperature for consistent classification
        )
        response = response_obj.text.strip()
        confidence = calculate_response_confidence(response, prompt)

    except Exception as e:
        logger.error(f"API Error: {e}. Using rule-based fallback.")
        response, confidence = rule_based_intent_detection(prompt)

    # Normalize separators and split into individual tasks
    # FIX: handle both " , " and "," and ", " as separators
    response = response.replace("\n", " ")
    raw_tasks = [t.strip() for t in response.replace(",", " , ").split(" , ") if t.strip()]

    # Filter to only valid recognized intents
    result = []
    for task in raw_tasks:
        matched = parse_intent(task, funcs)
        if matched:
            result.append({"intent": matched, "confidence": confidence})

    # Fallback: if nothing matched, treat entire prompt as general query
    if not result:
        logger.warning(f"No valid intent found for prompt: '{prompt}'. Defaulting to general.")
        result.append({"intent": f"general {prompt}", "confidence": 0.8})

    return result


if __name__ == "__main__":
    while True:
        print(FirstLayerDMM(input(">>> ")))
