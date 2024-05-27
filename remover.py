import os
import json
import requests
from rembg import remove
from PIL import Image
from colorama import init, Fore, Style

# Initialize colorama
init()

# Download image from URL and save it to the inputs folder
def download_image(url, filename, input_folder='inputs'):
    response = requests.get(url)
    input_path = os.path.join(input_folder, filename)
    with open(input_path, 'wb') as f:
        f.write(response.content)
    return input_path

# Process the image
def process_image(input_filename):
    input_image = Image.open(input_filename)
    output_image = remove(input_image)
    output_folder = 'outputs'
    output_filename = os.path.splitext(os.path.basename(input_filename))[0] + '_output.png'
    output_path = os.path.join(output_folder, output_filename)
    output_image.save(output_path)
    print(f"{Style.RESET_ALL}{Fore.GREEN}{input_filename}{Style.RESET_ALL} processed and saved as {Fore.GREEN}{output_path}{Style.RESET_ALL}.")

# Process URLs from JSON file
def process_urls_from_json(json_file):
    with open(json_file, 'r') as f:
        urls = json.load(f)
        for i, url in enumerate(urls):
            input_filename = f'input_image_{i}.jpg'
            input_path = download_image(url, input_filename)
            process_image(input_path)

# Define the JSON file name and path
json_file = 'urls.json'  # JSON file name
json_path = 'urls.json'  # JSON file path

# Process URLs from the JSON file
# process_urls_from_json(json_path)

# Process all images in the inputs folder
def process_images_from_folder(input_folder):
    for filename in os.listdir(input_folder):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            input_filename = os.path.join(input_folder, filename)
            process_image(input_filename)

# Get user input for processing method
option = input("Enter 'json' to process URLs from a JSON file, "
               "or 'inputs' to process images from the inputs folder: ")

if option == 'json':
    json_file = input("Enter the name of the JSON file containing URLs: ")
    process_urls_from_json(json_file)
elif option == 'inputs':
    input_folder = 'inputs'
    process_images_from_folder(input_folder)
else:
    print("Invalid option.")
