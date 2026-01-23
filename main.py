from Frontend.GUI import (
    GraphicalUserInterface,
    SetAssistantStatus,
    ShowTextToScreen,
    TempDirectoryPath,
    SetMicrophoneStatus,
    AnswerModifier,
    QueryModifier,
    GetMicrophoneStatus,
    GetAssistantStatus )
from Backend.Model import FirstLayerDMM
from Backend.RealTimeSearchEngine import RealTimeSearchEngine
from Backend.Automation import Automation
from Backend.SpeechToText import SpeechRecognition
from Backend.ChatBot import ChatBot
from Backend.TextToSpeech import TextToSpeech
from Backend.Productivity import ProductivityManager
from dotenv import dotenv_values
from asyncio import run
from time import sleep
import subprocess
import threading
import json
import os
from utils.logger import get_logger
from config.settings import CHAT_LOG_PATH

env_vars = dotenv_values(".env")
logger = get_logger()
Username = env_vars.get("Username")
Assistantname = "VYOM"
text_query_file = TempDirectoryPath('TextQuery.data')
DefaultMessage = f'''{Username} : Hello {Assistantname}, How are you?
{Assistantname} : Welcome {Username}. I am doing well. How may i help you?'''
subprocesses = []
Functions = ["open", "close", "play", "system", "content", "google search", "youtube search"]

# Confidence thresholds
HIGH_CONFIDENCE = 0.75
LOW_CONFIDENCE = 0.45

# Conversational state
pending_intent = None

def ShowDefaultChatIfNoChats():
    file = open(CHAT_LOG_PATH, 'r', encoding='utf-8')
    if len(file.read())<5:
        with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:
            file.write("")
        
        with open(TempDirectoryPath('Responses.data'), 'w', encoding='utf-8') as file:
            file.write(DefaultMessage)

def ReadChatLogJson():
    with open(CHAT_LOG_PATH, 'r', encoding='utf-8') as file:
            chatlog_data = json.load(file)
    return chatlog_data

def ChatLogIntegration():
    json_data = ReadChatLogJson()
    formatted_chatlog = ""
    for entry in json_data:
        if entry["role"] == "user":
            formatted_chatlog += f"User: {entry['content']}\n"
        elif entry["role"] == "assistant":
            formatted_chatlog += f"Assistant: {entry['content']}\n"
    formatted_chatlog = formatted_chatlog.replace("User",Username + " ")
    
    formatted_chatlog = formatted_chatlog.replace("Assistant", Assistantname + " ")
    
    with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:
        file.write(AnswerModifier(formatted_chatlog))

def ShowChatsOnGUI():
    file = open(TempDirectoryPath('Database.data'),'r', encoding='utf-8')
    Data = file.read()
    if len(str(Data))>0:
        lines = Data.split('\n')
        result = '\n'.join(lines)
        file.close()
        file = open(TempDirectoryPath('Responses.data'),'w', encoding='utf-8')
        file.write(result)
        file.close()

def InitialExecution():
    SetMicrophoneStatus("False")
    ShowTextToScreen("")
    ShowDefaultChatIfNoChats()
    ChatLogIntegration()
    ShowChatsOnGUI()

InitialExecution()

def ask_clarification(intent):
    clarifications = {
        "general": "Are you asking a general question or need help with something specific?",
        "realtime": "Are you looking for current information or news?",
        "open": "Do you want to open an application or website?",
        "close": "Do you want to close an application?",
        "play": "Should I play music or a video?",
        "system": "Are you referring to system controls like volume or brightness?",
        "content": "Do you want me to write or generate content?",
        "google search": "Are you searching the web?",
        "youtube search": "Are you looking for videos on YouTube?",
        "todo": "Do you want to manage your tasks?",
        "note": "Are you working with notes?",
    }
    return clarifications.get(intent.split()[0], "Could you clarify what you want to do?")

def ask_rephrase():
    return "I'm not sure what you mean. Could you rephrase your request?"

def handle_command_with_confidence(decisions, query):
    global pending_intent

    # Check if this is a response to a pending clarification
    if pending_intent:
        if query.lower().strip() in ["yes", "sure", "okay", "go ahead"]:
            # User confirmed, execute pending intent
            intent = pending_intent
            pending_intent = None
            return execute_intent(intent)
        elif query.lower().strip() in ["no", "cancel", "nevermind"]:
            # User declined
            pending_intent = None
            response = "Okay, let me know if there's something else I can help with."
            ShowTextToScreen(f"{Assistantname} : {response}")
            SetAssistantStatus("Answering ...")
            TextToSpeech(response)
            return True
        else:
            # Assume user is providing clarification, but for now treat as new query
            pending_intent = None

    # Process new decisions
    for decision in decisions:
        intent = decision["intent"]
        confidence = decision["confidence"]

        if confidence >= HIGH_CONFIDENCE:
            return execute_intent(intent)
        elif confidence >= LOW_CONFIDENCE:
            # Ask for clarification
            clarification = ask_clarification(intent)
            pending_intent = intent
            ShowTextToScreen(f"{Assistantname} : {clarification}")
            SetAssistantStatus("Answering ...")
            TextToSpeech(clarification)
            return True
        else:
            # Ask to rephrase
            rephrase_msg = ask_rephrase()
            ShowTextToScreen(f"{Assistantname} : {rephrase_msg}")
            SetAssistantStatus("Answering ...")
            TextToSpeech(rephrase_msg)
            return True

    return False

def execute_intent(intent):
    TaskExecution = False
    ImageExecution = False
    ImageGenerationQuery = ""

    # Initialize ProductivityManager
    productivity = ProductivityManager()

    # Handle productivity-related commands (assume high confidence)
    if intent.startswith("todo "):
        task = intent[5:]  # Remove "todo " prefix
        response = productivity.add_todo(task)
        ShowTextToScreen(f"{Assistantname} : {response}")
        SetAssistantStatus("Answering ...")
        TextToSpeech(response)
        return True

    elif intent == "list todos":
        response = productivity.list_todos()
        ShowTextToScreen(f"{Assistantname} : {response}")
        SetAssistantStatus("Answering ...")
        TextToSpeech(response)
        return True

    elif intent.startswith("complete todo "):
        task_id = int(intent[13:])  # Remove "complete todo " prefix
        response = productivity.complete_todo(task_id)
        ShowTextToScreen(f"{Assistantname} : {response}")
        SetAssistantStatus("Answering ...")
        TextToSpeech(response)
        return True

    elif intent.startswith("delete todo "):
        task_id = int(intent[11:])  # Remove "delete todo " prefix
        response = productivity.delete_todo(task_id)
        ShowTextToScreen(f"{Assistantname} : {response}")
        SetAssistantStatus("Answering ...")
        TextToSpeech(response)
        return True

    elif intent.startswith("note "):
        note_content = intent[5:]  # Remove "note " prefix
        if ":" in note_content:
            title, content = note_content.split(":", 1)
            response = productivity.add_note(title.strip(), content.strip())
            ShowTextToScreen(f"{Assistantname} : {response}")
            SetAssistantStatus("Answering ...")
            TextToSpeech(response)
            return True

    elif intent == "list notes":
        response = productivity.list_notes()
        ShowTextToScreen(f"{Assistantname} : {response}")
        SetAssistantStatus("Answering ...")
        TextToSpeech(response)
        return True

    elif intent.startswith("delete note "):
        title = intent[11:].strip()  # Remove "delete note " prefix
        logger.info(f"Attempting to delete note with title: {title}")
        response = productivity.delete_note(title)
        ShowTextToScreen(f"{Assistantname} : {response}")
        SetAssistantStatus("Answering ...")
        TextToSpeech(response)
        return True

    if "generate " in intent:
        ImageGenerationQuery = str(intent)
        ImageExecution = True

    if TaskExecution == False:
        if any(intent.startswith(func) for func in Functions):
            run(Automation([intent]))  # Pass as list for compatibility
            TaskExecution = True

    if ImageExecution == True:
        with open(os.path.join("Frontend", "Files", "ImageGeneration.data"), "w") as file:
            file.write(f"{ImageGenerationQuery},True")

        try:
            p1 = subprocess.Popen(['python', os.path.join('Backend', 'ImageGeneration.py')],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                stdin=subprocess.PIPE, shell=True)
            subprocesses.append(p1)

        except Exception as e:
            logger.error(f"Error starting ImageGeneration.py: {e}")

    if "general" in intent:
        SetAssistantStatus("Thinking ...")
        QueryFinal = intent.replace("general ", "")
        Answer = ChatBot(QueryModifier(QueryFinal))
        ShowTextToScreen(f"{Assistantname} : {Answer}")
        SetAssistantStatus("Answering ...")
        TextToSpeech(Answer)
        return True

    elif "realtime" in intent:
        SetAssistantStatus("Searching ...")
        QueryFinal = intent.replace("realtime ","")
        Answer = RealTimeSearchEngine(QueryModifier(QueryFinal))
        ShowTextToScreen(f"{Assistantname} : {Answer}")
        SetAssistantStatus("Answering ...")
        TextToSpeech(Answer)
        return True

    elif "exit" in intent:
        QueryFinal = "Okay, Bye!"
        Answer = ChatBot(QueryModifier(QueryFinal))
        ShowTextToScreen(f"{Assistantname} : {Answer}")
        SetAssistantStatus("Answering ...")
        TextToSpeech(Answer)
        SetAssistantStatus("Answering ...")
        os._exit(1)

    return False

def MainExecution():

    SetAssistantStatus("Listening ...")
    Query = SpeechRecognition()
    ShowTextToScreen(f"{Username} : {Query}")
    SetAssistantStatus("Thinking ...")
    Decision = FirstLayerDMM(Query)

    logger.info(f"Decision: {Decision}")
    
    G = any([i for i in Decision if i.startswith("general")])
    R = any([i for i in Decision if i.startswith("realtime")])
    
    Mearged_query = " and ".join(
        [" ".join(i.split()[1:]) for i in Decision if i.startswith("general") or i.startswith("realtime")]
    )
    
    # Initialize ProductivityManager
    productivity = ProductivityManager()
    
    # Handle productivity-related commands
    for command in Decision:
        cmd = command.strip()
        parts = cmd.split() # handles multiple spaces automatically

        #todo <task....>
        if parts and parts[0] == "todo":
            task = " ".join(parts[1:]).strip()
            if not task:
                response = "Please provide a todo. Example: todo buy milk"
            else: 
                response = productivity.add_todo(task)

            ShowTextToScreen(f"{Assistantname} : {response}")
            SetAssistantStatus("Answering ...")
            TextToSpeech(response)
            return True
        
        #list todos
        elif cmd == "list todos":
            response = productivity.list_todos()
            ShowTextToScreen(f"{Assistantname} : {response}")
            SetAssistantStatus("Answering ...")
            TextToSpeech(response)
            return True
            
        #complete todo <id>
        elif len(parts) == 3 and parts[0] == "complete" and parts[1] == "todo":
            task_id_str = parts[2].strip()
            if not task_id_str.isdigit():
                response = "Please provide a valid todo id. Example: complete todo 2"
            else:
                response = productivity.complete_todo(int(task_id_str))

            ShowTextToScreen(f"{Assistantname} : {response}")
            SetAssistantStatus("Answering ...")
            TextToSpeech(response)
            return True

        # delete todo <id>
        elif len(parts) >= 3 and parts[0] == "delete" and parts[1] == "todo":
        
            task_id_str = parts[2].strip()
            if not task_id_str.isdigit():
                response = "Please provide a valid todo id. Example: delete todo 3"
            else:
                response = productivity.delete_todo(int(task_id_str))

            ShowTextToScreen(f"{Assistantname} : {response}")
            SetAssistantStatus("Answering ...")
            TextToSpeech(response)
            return True

        # note 
        elif parts and parts[0] == "note":
            note_content = cmd[len("note"):].strip()  # keeps ":" structure intact
            if ":" not in note_content:
                response = "Please use format: note Title: content"
            else:
                title, content = note_content.split(":", 1)
                response = productivity.add_note(title.strip(), content.strip())

            ShowTextToScreen(f"{Assistantname} : {response}")
            SetAssistantStatus("Answering ...")
            TextToSpeech(response)
            return True
        
        #list notes 
        elif cmd == "list notes":
            response = productivity.list_notes()
            ShowTextToScreen(f"{Assistantname} : {response}")
            SetAssistantStatus("Answering ...")
            TextToSpeech(response)
            return True
        
        #delete note 
        elif len(parts) >= 3 and parts[0] == "delete" and parts[1] == "note":
            title = " ".join(parts[2:]).strip()
            if not title:
                response = "Please provide a note title. Example: delete note Meeting"
            else:
                logger.info(f"Attempting to delete note with title: {title}")
                response = productivity.delete_note(title)

            ShowTextToScreen(f"{Assistantname} : {response}")
            SetAssistantStatus("Answering ...")
            TextToSpeech(response)
            return True
    
    for queries in Decision:
        if "generate " in queries:
            ImageGenerationQuery = str(queries)
            ImageExecution = True
    
    for queries in Decision:
        if TaskExecution == False:
            if any(queries.startswith(func) for func in Functions):
                run(Automation(list(Decision)))
                TaskExecution = True
    
    if ImageExecution == True:

        with open(os.path.join("Frontend", "Files", "ImageGeneration.data"), "w") as file:
            file.write(f"{ImageGenerationQuery},True")

        try:
            p1 = subprocess.Popen(['python', os.path.join('Backend', 'ImageGeneration.py')],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                stdin=subprocess.PIPE, shell=True)
            subprocesses.append(p1)

        except Exception as e:
            logger.error(f"Error starting ImageGeneration.py: {e}")

def CheckTextQuery():
    try:
        if os.path.exists(text_query_file):
            with open(text_query_file, 'r', encoding='utf-8') as file:
                query = file.read().strip()
            if query:
                # Remove the file after reading
                os.remove(text_query_file)
                return query
    except Exception as e:
        logger.error(f"Error reading text query: {e}")
    return None

def FirstThread():

    while True:

        # Check for text queries first
        text_query = CheckTextQuery()
        if text_query:
            SetAssistantStatus("Thinking ...")
            ShowTextToScreen(f"{Username} : {text_query}")
            Decision = FirstLayerDMM(text_query)
            logger.info(f"Text Decision: {Decision}")
            handle_command_with_confidence(Decision, text_query)
            continue

        CurrentStatus = GetMicrophoneStatus()

        if CurrentStatus == "True":
            MainExecution()

        else:
            AIStatus = GetAssistantStatus()

            if "Available ..." in AIStatus:
                sleep(0.1)

            else:
                SetAssistantStatus("Available ...")

def SecondThread():
    
    GraphicalUserInterface()

if __name__ == "__main__":
    thread2 = threading.Thread(target=FirstThread, daemon=True)
    thread2.start()
    SecondThread()