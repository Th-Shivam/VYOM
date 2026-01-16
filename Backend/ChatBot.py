from groq import Groq
from json import load , dump
import datetime
import os
from dotenv import dotenv_values
from utils.logger import get_logger
from utils.memory import MemoryManager
import time

# File config variables
MAX_ATTEMPTS = 3 # number of maximum chatbot retries
COOLDOWN_SECONDS = 5 # cooldown seconds between failed attempts

#load env vars fromm the .env file

env_vars = dotenv_values(".env")

#retrieve specific env vars for username , assistant name and API Key

Username = env_vars.get("Username")
AssistantName = env_vars.get("AssistantName")
GroqAPIKey = env_vars.get("GroqAPIKey")

#initialize the Groq client with the API key
client =  Groq(api_key=GroqAPIKey)

# Initialize memory manager
memory_manager = MemoryManager()

#defiine a system msg that provides conext to the model about its role and behavior
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {AssistantName} Virtual Yet Omnipotent Machine  which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""


#a list of system inst for the chatbot 

SystemChatBot = [
    {"role":"system", "content": System },
]

# Attempt to load the chat history from a JSON file
chatlog_path = os.path.join("Data", "ChatLog.json")

# Load memory from file
memory_manager.load_from_file(chatlog_path)

# Function to get real time date and time info 

def RealTimeInformation():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y") 
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")

    #format the info into a string 

    data = f"Please use this real-time information if needed , \n"
    data += f"Day : {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours : {minute} minutes : {second} seconds\n"
    return data

#func to modify the chatbot's response for better formatting . 

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

def ChatBot(Query, attempt_count=1):
    #this function sends the user query to the Groq model and returns the response
    try:
        # Check for inactivity and clear memory if needed
        memory_manager.cleanup_if_inactive()

        # Add user query to memory
        memory_manager.add_message("user", Query)

        # Get current context
        messages = memory_manager.get_context()

        # makes a request to the Groq model with the messages and system context
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile" ,
            messages = SystemChatBot + [{"role": "system", "content": RealTimeInformation()}] + messages,
            max_tokens=1024 ,
            temperature=0.7,
            top_p=1 ,
            stream=True,
            stop=None
        )

        Answer = ""

        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</s>", "")

        # Add assistant response to memory
        memory_manager.add_message("assistant", Answer)

        # Save memory to file
        memory_manager.save_to_file(chatlog_path)

        return AnswerModifier(Answer = Answer)

    except Exception as e:
        logger = get_logger(__name__)
        logger.error(f"Attempt {attempt_count}/{MAX_ATTEMPTS} failed: {e}")
        # Clear memory on error
        memory_manager.memory.clear()
        memory_manager.save_to_file(chatlog_path)
        if attempt_count >= MAX_ATTEMPTS:
            logger.error("Maximum attempts exceeded. Giving up.")
            return "I apologize, I am experiencing some trouble generating this response. Please try again later"
        time.sleep(COOLDOWN_SECONDS)
        return ChatBot(Query, attempt_count+1)

if __name__ == "__main__":
    while True:
        user_input = input("Enter Your Question : ")
        print(ChatBot(user_input))
 
