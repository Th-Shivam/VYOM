

# VYOM Architecture


## Overview

    VYOM is an AI-powered virtual assistant isnpired by JARVIS

     It supports voice commands and chatbot interactions to respond to user queries.

     It also provides automation features, image generation, and real-time search capabilities.

     
     One of the speciall features of VYOM is its modular multi-threading architecture

     Different tasks run on separate threads which helps prevent system freezing and improves real-time responsiveness.




## Technical Architecture


     VYOM follows a modular architecture where different modules handle different tasks independently.

     VYOM uses multi-threading to prevent system freezing and ensure smooth performance with real-time responsiveness.

     Separate components are responsible for voice input, NLP processing, task execution, and GUI management.



## System Flow

  Voice Input → Speech To Text → NLP Processing → Action Execution → Text To Speech Output

   ## System Flow

    Voice Input → Speech To Text → NLP Processing → Action Execution → Text To Speech Output

    The system starts when the user gives a voice command through the microphone.

    The SpeechToText.py module converts the spoken audio into text.

    After that, the NLP processing layer analyzes the user’s intent and selects the appropriate module for the requested task. 
  
    The executor then performs the action, such as automation, chatbot response, image generation, or real-time search.
    
    Finally, the TextToSpeech.py module converts the generated response into voice output for the user.



## Multi-Threading Model

    VYOM uses a multi-threaded architecture to perform multiple tasks simultaneously without blocking the system.

   ### Listener Thread
         
         The listener thread continuously monitors the microphone for user voice commands and wake words.  

  ### Processor Thread  

        The processor thread handles NLP processing, AI model interaction, and intent recognition without interrupting the listener thread. 

  ### Executor Thread    
     
       The executor thread performs system tasks, automation features, and GUI updates based on the processed commands.




## Backend Module Responsibilities

  ### Automation.py
   
   Handles automation tasks and workflow execution within the assistant.

  ### ChatBot.py

    Manages chatbot conversations and generates responses for user queries.

  ### ImageGeneration.py

    Generates AI-based images using external models and APIs.

  ### Model.py

     Loads and manages AI, NLP, and machine learning models used in the project.

   ### Productivity.py

     Provides productivity-related features such as utilities, reminders, and task management.

   ### RealTimeSearchEngine.py

    Handles real-time web searches and processes online queries.

   ### SpeechToText.py

    Converts spoken audio input into text for further processing.

   ### TextToSpeech.py

    Converts text responses into spoken audio output for the user.     




## Frontend Components

  ### GUI.py
    
    Controls the graphical user interface and manages user interaction with the assistant.

  ### Graphics

    Stores graphical assets such as icons, images, logos, and animations used in the interface.

  ### Files/

    Stores runtime data and application state information such as responses, microphone status, and generated outputs.

  ### automation/

    Contains frontend automation and GUI testing scripts.

  ### playwright_tests/

    Includes Playwright-based UI testing files and screenshots for frontend validation.

  ### tests/

    Contains frontend test cases and issue-specific test scripts.





## Utilities and Configuration

  ### config/settings.py

    Stores centralized configuration variables and project settings.

  ### utils/logger.py

    Handles logging, debugging, and system monitoring functionalities.

  ### utils/memory.py

    Manages memory handling and conversational context within the assistant.

  ### .env.example

    Provides a sample environment variables file for API keys and configuration setup.    





## Technologies Used

- Python
- Groq AI
- Cohere AI
- Asyncio
- Threading
- NLP Pipeline
- Speech Recognition
- Text-to-Speech
- PyAudio
- FFmpeg 



## Conclusion

The modular and multi-threaded architecture of VYOM improves scalability, responsiveness, and overall system performance.

By separating voice input, processing, and execution into independent modules and threads, the assistant can handle tasks efficiently without freezing or blocking the user interface.