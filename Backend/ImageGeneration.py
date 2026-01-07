import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import get_key
import os
from time import sleep

# Function to open and display images based on a given prompt
def open_images(prompt):
    folder_path = r"Data"
    prompt = prompt.replace(" ", "_")
    files = [f"{prompt}{i}.jpg" for i in range(1, 5)]

    for jpg_file in files:
        image_path = os.path.join(folder_path, jpg_file)

        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)
        except Exception as e:
            print(f"❌ Image not found: {image_path} | Error: {e}")

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIKey')}"}

# Async function to send a query to the Hugging Face API
async def query(payload):
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.content
    else:
        print(f"❌ API Error {response.status_code}: {response.text}")
        return None

# Async function to generate images based on the given prompt
async def generate_images(prompt: str):
    tasks = []

    for _ in range(4):
        payload = {
            "inputs": f"{prompt}, quality=4K, sharpness=maximum, Ultra High details, high resolution, seed={randint(0, 1000000)}",
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)

    image_bytes_list = await asyncio.gather(*tasks)

    os.makedirs("Data", exist_ok=True)  # Ensure Data folder exists

    for i, image_bytes in enumerate(image_bytes_list):
        if image_bytes is not None:
            filename = os.path.join("Data", f"{prompt.replace(' ', '_')}{i + 1}.jpg")
            with open(filename, "wb") as image_file:
                image_file.write(image_bytes)
            print(f"✅ Image saved: {filename}")
        else:
            print(f"❌ Failed to generate image {i + 1}")

# Wrapper function to generate and open images
def GenerateImages(prompt: str):
    asyncio.run(generate_images(prompt))
    open_images(prompt)

# Main loop to monitor for image generation requests
while True:
    try:
        with open(os.path.join("Frontend", "files", "ImageGeneration.data"), "r") as f:
            Data: str = f.read()

        Prompt, Status = Data.strip().split(",")

        if Status == "True":
            print("🔄 Generating Images ...")
            GenerateImages(Prompt)

            with open(os.path.join("Frontend", "files", "ImageGeneration.data"), "w") as f:
                f.write(f"{Prompt},False")
            break

        else:
            sleep(1)

    except Exception as e:
        print(f"⚠️ Error: {e}")
