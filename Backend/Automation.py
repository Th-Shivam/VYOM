
import platform
import subprocess  # Import subprocess for interacting with the system.
import os  # Import os for operating system functionalities.

# Conditionally import AppOpener only on Windows
IS_WINDOWS = platform.system() == "Windows"
if IS_WINDOWS:
    from AppOpener import close, open as appopen

from webbrowser import open as webopen  # Import web browser functionality.
from pywhatkit import search, playonyt  # Import functions for search and YouTube playback.
from dotenv import dotenv_values  # Import dotenv to manage environment variables.
from bs4 import BeautifulSoup  # Import BeautifulSoup for parsing HTML content.
from rich import print  # Import rich for styled console output.
from groq import Groq  # Import Groq for AI Chat functionalities.
import webbrowser  # Import webbrowser for opening URLs.
import requests  # Import requests for making HTTP requests.
import keyboard  # Import keyboard for keyboard-related actions.
import asyncio  # Import asyncio for asynchronous programming.

# Load environment variables from the .env file.
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")  # Retrieve the Groq API key.

# Define CSS classes for parsing specific elements in HTML content.
classes = ["zCubwf", "hgKElc", "LTKOO sY7ric", "Z0LcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta",
           "IZ6rdc", "O5uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table__webanswers-table", "dDoNo ikb4Bb gsrt", "sXLaOe",
           "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

# Define a user-agent for making web requests.
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

# Initialize the Groq client with the API key.
client = Groq(api_key=GroqAPIKey)

# Predefined professional responses for user interactions.
professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need—don't hesitate to ask.",
]

# List to store chatbot messages.
messages = []

# System message to provide context to the chatbot using a cross-platform method to get the username.
try:
    current_user = os.getlogin()
except OSError:
    current_user = os.environ.get("USER", os.environ.get("USERNAME", "user"))

SystemChatBot = [{"role": "system", "content": f"Hello, I am {current_user}. You're a content writer. You have to write content like letters, codes , applications , emails, articles, and other professional documents as requested."}]

# Function to perform a Google search.
def GoogleSearch(Topic):
    search(Topic)  # Use pywhatkit's search function to perform a Google search.
    return True  # Indicate success.

# Function to generate content using AI and save it to a file.
def Content(Topic):
    
    # Nested function to open a file with the default text editor.
    def OpenFile(File):
        if IS_WINDOWS:
            # On Windows, use 'notepad.exe'.
            subprocess.Popen(['notepad.exe', File])
        else:
            # On Linux/macOS, use 'xdg-open', which uses the default application.
            subprocess.Popen(['xdg-open', File])
    
    # Nested function to generate content using the AI chatbot.
    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": f"{prompt}"})  # Add the user's prompt to messages.
        
        completion = client.chat.completions.create(
            model="llama3-70b-8192",  # Specify the AI model.
            messages=SystemChatBot + messages,  # Include system instructions and chat history.
            max_tokens=2048,  # Limit the maximum tokens in the response.
            temperature=0.7,  # Adjust response randomness.
            top_p=1,  # Use nucleus sampling for response diversity.
            stream=True,  # Enable streaming response.
            stop=None  # Allow the model to determine stopping conditions.
        )
        
        Answer = ""  # Initialize an empty string for the response.
        
       # Process streamed response chunks.
        for chunk in completion:
            if chunk.choices[0].delta.content:  # Check for content in the current chunk.
                Answer += chunk.choices[0].delta.content  # Append the content to the answer.

        Answer = Answer.replace("</s>", "")  # Remove unwanted tokens from the response.
        messages.append({"role": "assistant", "content": Answer})  # Add the AI's response to messages.
        return Answer

    Topic: str = Topic.replace("Content ", "")  # Remove 'Content ' from the topic.
    ContentByAI = ContentWriterAI(Topic)  # Generate content using AI.

    # Ensure the 'Data' directory exists
    if not os.path.exists("Data"):
        os.makedirs("Data")

    file_path = os.path.join("Data", f"{Topic.lower().replace(' ', '')}.txt")

    # Save the generated content to a text file.
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(ContentByAI)  # Write the content to the file.

    OpenFile(file_path)
    return True  # Indicate success.

def YoutubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(Url4Search)  # Open the YouTube search results in the web browser.
    return True  # Indicate success.

def PlayYoutube(query):
    playonyt(query)  # Use pywhatkit to play the specified topic on YouTube.
    return True  # Indicate success.

def OpenApp(app , sess=requests.session()):
    if IS_WINDOWS:
        try:
            appopen(app, match_closest=True, output=True)
            return True
        except:
            pass  # Fallback to web search
    else: # For Linux/macOS
        try:
            # On Linux, application commands are typically lowercase.
            app_command = app.lower().replace(" ", "")
            subprocess.Popen([app_command])
            return True
        except FileNotFoundError:
            # If the app isn't found locally, fall back to a web search.
            print(f"[bold yellow]App '{app}' not found locally. Searching online...[/bold yellow]")
            pass # Fallback to web search
    
    # Fallback web search logic if app fails to open
    def extract_links(html):
        if html is None:
            return []
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a', {'jsname':'UWckNb'})
        return [link.get('href') for link in links]

    def search_google(query):
        url = f"https://www.google.com/search?q={query}"
        headers = {"User-Agent" : useragent}
        response =  sess.get(url, headers=headers)

        if response.status_code == 200:
            return response.text
        else:
            print("[bold red]Failed to retrieve search results.[/bold red]")
        return None
    
    html = search_google(app)
    if html:
        try:
            link = extract_links(html)[0]
            webopen(link)
        except IndexError:
            print(f"[bold red]No web link found for '{app}'.[/bold red]")
    return True


def CloseApp(app):
    if IS_WINDOWS:
        if "chrome" in app:
            pass # Special handling can be added here if needed
        try:
            close(app, match_closest=True , output=True , throw_error = True)
            return True
        except:
            return False
    else: # For Linux/macOS
        try:
            # Use 'pkill' with '-i' for case-insensitive matching.
            subprocess.run(["pkill", "-i", app], check=True, capture_output=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Fails if pkill command fails or process is not found.
            return False
        
def System(command):
    # This function uses the 'keyboard' library which might require root privileges on Linux.
    # An alternative for volume control on Linux is using 'amixer' or 'pactl' commands.
    # For now, we'll keep it as is, but be aware of potential permission issues.
    try:
        if command == "mute":
            keyboard.press_and_release("volume mute")
        elif command == "unmute":
            keyboard.press_and_release("volume mute")
        elif command == "volume up":
            keyboard.press_and_release("volume up")
        elif command == "volume down":
            keyboard.press_and_release("volume down")
        return True
    except Exception as e:
        print(f"[bold red]System command failed: {e}[/bold red]")
        print("[bold yellow]On Linux, this may require running the script with 'sudo' privileges.[/bold yellow]")
        return False


async def TranslateAndExecute(commands: list[str]):
    funcs = []

    for command in commands:
        if command.startswith("open "):
            if "open it" in command:
                pass
            elif "open file" in command:
                pass
            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))
                funcs.append(fun)
        elif command.startswith("general "):
            pass
        elif command.startswith("realtime "):
            pass
        elif command.startswith("close "):
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))
            funcs.append(fun)
        elif command.startswith("play "):
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play "))
            funcs.append(fun)
        elif command.startswith("content "):
            fun = asyncio.to_thread(Content, command.removeprefix("content "))
            funcs.append(fun)
        elif command.startswith("google search "):
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))
            funcs.append(fun)
        elif command.startswith("youtube search "):
            fun = asyncio.to_thread(YoutubeSearch, command.removeprefix("youtube search "))
            funcs.append(fun)
        elif command.startswith("system "):
            fun = asyncio.to_thread(System, command.removeprefix("system "))
            funcs.append(fun)
        else:
            print(f"No Functions Found For {command}")
    
    if funcs:
        results = await asyncio.gather(*funcs)
        for result in results:
            if isinstance(result, str):
                yield result
            else:
                yield result

async def Automation(commands: list[str]):
    async for result in TranslateAndExecute(commands):
        pass

    return True

# Example of how to run the automation (add this if you don't have a main execution block)
if __name__ == "__main__":
    # Example commands to test the functions
    # To run this, you would call asyncio.run(Automation(test_commands))
    test_commands = [
        # "open firefox", # Example for Linux
        # "open vscode", # This may need to be 'code' on Linux
        # "close firefox",
        # "content about python programming"
    ]
    if test_commands:
        print("Running example commands...")
        asyncio.run(Automation(test_commands))
        print("Example commands finished.")
    else:
        print("No example commands to run. The script is ready.") 
