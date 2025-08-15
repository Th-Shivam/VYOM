from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import mtranslate as mt
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load environment variables from the .env file.
env_vars = dotenv_values(".env")
# Get the input language setting from the environment variables.
InputLanguage = env_vars.get("InputLanguage")

# Define the HTML code for the speech recognition interface.
HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new webkitSpeechRecognition() || new SpeechRecognition();
            recognition.lang = '';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            recognition.stop();
            output.innerHTML = "";
        }
    </script>
</body>
</html>'''

# Replace the language setting in the HTML code with the input language from the environment variables.
HtmlCode = str(HtmlCode).replace("recognition.lang = '';", f"recognition.lang = '{InputLanguage}';")

# Get the current working directory.
current_dir = os.getcwd()

# ✨ Use os.path.join for cross-platform compatibility
data_dir = os.path.join(current_dir, "Data")
os.makedirs(data_dir, exist_ok=True) # Ensure the directory exists
voice_html_path = os.path.join(data_dir, "Voice.html")

# Write the modified HTML code to a file.
with open(voice_html_path, "w") as f:
    f.write(HtmlCode)

# Generate the file path for the HTML file.
Link = f"file:///{voice_html_path}"

# Set Chrome options for the WebDriver.
chrome_options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36"
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")

# ✨ REMOVED: The hardcoded Windows path is no longer needed.
# chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# Initialize the Chrome WebDriver. WebDriver Manager will find Chrome automatically.
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# ✨ Use os.path.join for cross-platform compatibility
TempDirPath = os.path.join(current_dir, "Frontend", "Files")
os.makedirs(TempDirPath, exist_ok=True) # Ensure the directory exists

# Function to set the assistants status by writing it into a file
def SetAssistantStatus(Status):
    status_file_path = os.path.join(TempDirPath, "Status.data")
    with open(status_file_path, "w" , encoding='utf-8') as file:
        file.write(Status)

# Function to modify a query to ensure proper punctuation and formatting.
def QueryModifier(Query):
    new_query = Query.lower().strip()
    if not new_query:
        return ""
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you", "what's", "wh"]
    
    # Check if the query is a question and add a question mark if necessary.
    if any(word in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        # Add a period if the query is not a question.
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."
    
    return new_query.capitalize()

# Translator   
def UniversalTranslator(Text):
    english_translation = mt.translate(Text, "en" , "auto")
    return english_translation.capitalize()

def SpeechRecognition():
    # Open the HTML file in the browser 
    driver.get(Link)

    # ✅ Wait for the start button to be present and clickable
    try:
        start_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "start"))
        )
        start_button.click()
    except Exception as e:
        print("Start button not found or not clickable:", e)
        return ""

    while True:
        try:
            Text = driver.find_element(by=By.ID , value="output").text
            if Text:
                driver.find_element(by=By.ID , value="end").click()
                
                if InputLanguage and (InputLanguage.lower() == "en" or "en" in InputLanguage.lower()):
                    return QueryModifier(Text)
                else:
                    SetAssistantStatus("Translating")
                    return QueryModifier(UniversalTranslator(Text))
        except Exception:
            pass

if __name__ == "__main__":
    while True:
        Text = SpeechRecognition()
        if Text:
            print(Text)
