import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import get_key
import os
from time import sleep

# Function to open and display images based on a given prompt
def open_images(prompt):
    folder_path = r"Data"  # Folder where the images are stored
    prompt = prompt.replace(" ", "_")  # Replace spaces in prompt with underscores
    
    # Generate the filenames for the images
    files = [f"{prompt}{i}.jpg" for i in range(1, 5)]
    
    for jpg_file in files:
        image_path = os.path.join(folder_path, jpg_file)
        
        try:
            # Try to open the image
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()  # Display the image
            sleep(1)

        except:
            # Handle exception
            print(f"Image not found: {image_path}")

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIKey')}"}

# Async function to send a query to the Hugging Face API
async def query(payload):
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
    return response.content

# Async function to generate images based on the given prompt
async def generate_images(prompt: str):
    tasks = []
    
    # Create 4 image generation tasks
    for _ in range(4):
        payload = {
            "inputs": f"{prompt}, quality=4K, sharpness=maximum, Ultra High details, high resolution, seed = {randint(0, 1000000)}"
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)
    
    # Wait for all tasks to complete
    image_bytes_list = await asyncio.gather(*tasks)
    
    # Save the generated images to files
    for i, image_bytes in enumerate(image_bytes_list):
        with open(fr"Data\{prompt.replace(' ', '_')}{i + 1}.jpg", "wb") as image_file:
            image_file.write(image_bytes)

# Wrapper function to generate and open images
def GenerateImages(prompt: str):
    asyncio.run(generate_images(prompt))  # Run the async image generation
    open_images(prompt)  # Open the generated images

# Main loop to monitor for image generation requests
while True:
    
    try:
        # Read the status and prompt from the data file
        with open(r"Frontend\Files\ImageGeneration.data", "r") as f:
            Data: str = f.read()
        
        Prompt, Status = Data.split(",")
        
        # If the status indicates an image generation request
        if Status == "True":
            print("Generating Images ... ")
            ImageStatus = GenerateImages(Prompt)

            with open(r"Frontend\Files\ImageGeneration.data", "w") as f:
                f.write(f"{Prompt},False")
                break

        else:
            sleep(1)

    except Exception as e:
        print(f"An error occurred: {e}")
        break