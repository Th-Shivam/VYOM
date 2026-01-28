import cohere
from rich import print
from dotenv import dotenv_values
from utils.logger import get_logger

env_vars = dotenv_values(".env")

CohereAPIKey = env_vars.get("CohereAPIKey")

co = cohere.Client(api_key=CohereAPIKey)

logger = get_logger()

# List of functions to be used in the model

funcs = [
    "exit" , "general" , "realtime" , "open" , "close" , "play" , "generate image" , "system" , "content" , "google search" , "youtube search" , "reminder",
    "todo", "note", "list todos", "list notes", "complete todo", "delete note", "delete todo"
]

#initialize an emppty list to store messages 

messages = []

#define the preamble that guides the model how to categorize the queries 

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
- 'exit' - For ending conversation

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

Respond with ONLY the category and content, nothing else.
"""

#define a chat history with predefined user-chatbot interactions for context . 

ChatHistory = [
    {"role" : "User" , "message":"how are you ?"} ,
    {"role" : "Chatbot" , "message":"general how are you ?"} ,
    {"role" : "User" , "message":"do you like pizza ?"} , 
    {"role" : "Chatbot" , "message":"general do you like pizza ?"} ,
    {"role" : "User" , "message":"open chrome and tell me about mahatma gandhi"} , 
    {"role" : "Chatbot" , "message":"open chrome , general who is mahatma gandhi ."} ,
    {"role" : "User" , "message":"open chrome and firefox"} ,
    {"role" : "Chatbot" , "message":"open chrome , open firefox"},
    {"role" : "User" , "message":"what is today's date and by the way remind me that i have a dancing performance on 5th augusst 11:00 pm" }, 
    {"role" : "Chatbot" , "message":"general what is today's date , reminder 11:00 pm 5th august  dancing performance" } ,
    {"role" : "User" , "message":"chat with me "} , 
    {"role" : "Chatbot" , "message":"general chat with me"} 
    
]

def rule_based_intent_detection(prompt):
    """Simple rule-based intent detection as fallback when API fails"""
    prompt_lower = prompt.lower().strip()

    # Check for exit commands
    if any(word in prompt_lower for word in ["bye", "exit", "quit", "goodbye", "see you"]):
        return "exit", 0.9

    # Check for open commands
    if prompt_lower.startswith("open "):
        app = prompt_lower[5:].strip()
        return f"open {app}", 0.8

    # Check for close commands
    if prompt_lower.startswith("close "):
        app = prompt_lower[6:].strip()
        return f"close {app}", 0.8

    # Check for play commands
    if prompt_lower.startswith("play "):
        song = prompt_lower[5:].strip()
        return f"play {song}", 0.8

    # Check for generate image commands
    if "generate image" in prompt_lower or "create image" in prompt_lower:
        return f"generate image {prompt}", 0.7

    # Check for todo commands
    if "add a todo" in prompt_lower or "add todo" in prompt_lower:
        task = prompt.replace("add a todo", "").replace("add todo", "").strip()
        return f"todo {task}", 0.8

    if "list todos" in prompt_lower or "show my todos" in prompt_lower:
        return "list todos", 0.9

    # Check for realtime queries (news, current info)
    if any(word in prompt_lower for word in ["news", "today", "current", "latest", "who is", "what is"]):
        return f"realtime {prompt}", 0.6

    # Default to general with higher confidence
    return f"general {prompt}", 0.8

def calculate_response_confidence(response, prompt):
    """Calculate confidence score based on response quality and prompt matching"""
    response_lower = response.lower().strip()
    prompt_lower = prompt.lower().strip()

    # High confidence if response directly matches expected format
    if any(response_lower.startswith(func) for func in funcs):
        # Check if the response contains the original prompt or similar content
        if prompt_lower in response_lower or any(word in response_lower for word in prompt_lower.split()):
            return 0.9
        else:
            return 0.8

    # Medium confidence for partial matches
    if any(func in response_lower for func in funcs):
        return 0.7

    # Lower confidence for ambiguous responses
    if len(response.split()) < 3:
        return 0.5

    # Default confidence
    return 0.6

#define the main function that will be used for decision making in queries

def FirstLayerDMM(prompt : str = "test"):
    #add the users query to the messages list
    messages.append({"role": "User", "content": f"{prompt}"})

    # Prepare messages for Chat API
    chat_messages = [
        {"role": "system", "content": preamble}
    ]

    # Add chat history
    for msg in ChatHistory:
        chat_messages.append({"role": "user", "content": msg["message"]})
        chat_messages.append({"role": "assistant", "content": "general " + msg["message"]})  # Simplified for history

    # Add current prompt
    chat_messages.append({"role": "user", "content": prompt})

    # Try API first, fallback to rule-based if API fails
    try:
        # Prepare chat history for Cohere API
        chat_history = []
        for msg in chat_messages[1:]:  # Skip the system message
            if msg["role"] == "user":
                chat_history.append({"role": "USER", "message": msg["content"]})
            elif msg["role"] == "assistant":
                chat_history.append({"role": "CHATBOT", "message": msg["content"]})

        response_obj = co.chat(
            model="command-r-08-2024",
            message=prompt,
            chat_history=chat_history,
            max_tokens=100,
            temperature=0.7,
        )
        response = response_obj.text.strip()
        # Calculate confidence based on response quality
        confidence = calculate_response_confidence(response, prompt)
        use_api = True
    except Exception as e:
        logger.error(f"API Error: {e}. Using rule-based fallback.")
        # Rule-based fallback for basic intent detection
        intent, confidence = rule_based_intent_detection(prompt)
        # Format as string to match API response processing
        response = intent
        use_api = False

    #remove newline characters and split response
    response = response.replace("\n", " ")
    response = response.split(" , ")

    #strip leading and trailing whitespace from each task
    response = [i.strip() for i in response]

    #initialize an empty list to filter valid tasks .
    temp = []

    #filter the tasks based on recognized functions keywords .
    for task in response:
        # Split the task into type and content
        parts = task.split(" ", 1)
        if len(parts) == 2:
            intent_type, content = parts
            if intent_type in funcs:
                # For general/realtime, keep the full query, for others use the content
                if intent_type in ["general", "realtime"]:
                    temp.append({"intent": f"{intent_type} {content}", "confidence": confidence})
                else:
                    temp.append({"intent": f"{intent_type} {content}", "confidence": confidence})
        elif task in funcs:
            temp.append({"intent": task, "confidence": confidence})

    # If no valid tasks found, create a default general intent
    if not temp:
        temp.append({"intent": f"general {prompt}", "confidence": 0.8})

    #update the response with the filtered tasks
    response = temp

    return response


if __name__ == "__main__":
    while True:
        print(FirstLayerDMM(input(">>> ")))