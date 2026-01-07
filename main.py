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

env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = "VYOM"
DefaultMessage = f'''{Username} : Hello {Assistantname}, How are you?
{Assistantname} : Welcome {Username}. I am doing well. How may i help you?'''
subprocesses = []
Functions = ["open", "close", "play", "system", "content", "google search", "youtube search"]

def ShowDefaultChatIfNoChats():
    file = open(os.path.join('Data', 'ChatLog.json'),'r', encoding='utf-8')
    if len(file.read())<5:
        with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:
            file.write("")
        
        with open(TempDirectoryPath('Responses.data'), 'w', encoding='utf-8') as file:
            file.write(DefaultMessage)

def ReadChatLogJson():
    with open(os.path.join('Data', 'ChatLog.json'), 'r', encoding='utf-8') as file:
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

def MainExecution():
    
    TaskExecution = False
    ImageExecution = False
    ImageGenerationQuery = ""
    
    SetAssistantStatus("Listening ...")
    Query = SpeechRecognition()
    ShowTextToScreen(f"{Username} : {Query}")
    SetAssistantStatus("Thinking ...")
    Decision = FirstLayerDMM(Query)
    
    print("")
    print(f"Decision : {Decision}")
    print("")
    
    G = any([i for i in Decision if i.startswith("general")])
    R = any([i for i in Decision if i.startswith("realtime")])
    
    Mearged_query = " and ".join(
        [" ".join(i.split()[1:]) for i in Decision if i.startswith("general") or i.startswith("realtime")]
    )
    
    # Initialize ProductivityManager
    productivity = ProductivityManager()
    
    # Handle productivity-related commands
    for command in Decision:
        if command.startswith("todo "):
            task = command[5:]  # Remove "todo " prefix
            response = productivity.add_todo(task)
            ShowTextToScreen(f"{Assistantname} : {response}")
            SetAssistantStatus("Answering ...")
            TextToSpeech(response)
            return True
            
        elif command == "list todos":
            response = productivity.list_todos()
            ShowTextToScreen(f"{Assistantname} : {response}")
            SetAssistantStatus("Answering ...")
            TextToSpeech(response)
            return True
            
        elif command.startswith("complete todo "):
            task_id = int(command[13:])  # Remove "complete todo " prefix
            response = productivity.complete_todo(task_id)
            ShowTextToScreen(f"{Assistantname} : {response}")
            SetAssistantStatus("Answering ...")
            TextToSpeech(response)
            return True
            
        elif command.startswith("delete todo "):
            task_id = int(command[11:])  # Remove "delete todo " prefix
            response = productivity.delete_todo(task_id)
            ShowTextToScreen(f"{Assistantname} : {response}")
            SetAssistantStatus("Answering ...")
            TextToSpeech(response)
            return True
            
        elif command.startswith("note "):
            note_content = command[5:]  # Remove "note " prefix
            if ":" in note_content:
                title, content = note_content.split(":", 1)
                response = productivity.add_note(title.strip(), content.strip())
                ShowTextToScreen(f"{Assistantname} : {response}")
                SetAssistantStatus("Answering ...")
                TextToSpeech(response)
                return True
            
        elif command == "list notes":
            response = productivity.list_notes()
            ShowTextToScreen(f"{Assistantname} : {response}")
            SetAssistantStatus("Answering ...")
            TextToSpeech(response)
            return True
            
        elif command.startswith("delete note "):
            # Extract the title from the command
            title = command[11:].strip()  # Remove "delete note " prefix and any extra spaces
            print(f"Attempting to delete note with title: {title}")
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
            print(f"Error starting ImageGeneration.py: {e}")
    
    if G and R:
        
        SetAssistantStatus("Searching ...")
        Answer = RealTimeSearchEngine(QueryModifier(Mearged_query))
        ShowTextToScreen(f"{Assistantname} : {Answer}")
        SetAssistantStatus("Answering ...")
        TextToSpeech(Answer)
        return True
    
    else:
        for Queries in Decision:
            
            if "general" in Queries:
                SetAssistantStatus("Thinking ...")
                QueryFinal = Queries.replace("general ", "")
                Answer = ChatBot(QueryModifier(QueryFinal))
                ShowTextToScreen(f"{Assistantname} : {Answer}")
                SetAssistantStatus("Answering ...")
                TextToSpeech(Answer)
                return True
            
            elif "realtime" in Queries:
                SetAssistantStatus("Searching ...")
                QueryFinal = Queries.replace("realtime ","")
                Answer = RealTimeSearchEngine(QueryModifier(QueryFinal))
                ShowTextToScreen(f"{Assistantname} : {Answer}")
                SetAssistantStatus("Answering ...")
                TextToSpeech(Answer)
                return True
            
            elif "exit" in Queries:
                QueryFinal = "Okay, Bye!"
                Answer = ChatBot(QueryModifier(QueryFinal))
                ShowTextToScreen(f"{Assistantname} : {Answer}")
                SetAssistantStatus("Answering ...")
                TextToSpeech(Answer)
                SetAssistantStatus("Answering ...")
                os._exit(1)

def FirstThread():
    
    while True:
        
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