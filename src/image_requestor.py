import requests
import os
import random
import re

def select_random_image(taxon_key, limit=100000):
    """
    Fetches images for a given taxon key from the GBIF API and randomly selects one of them
    
    Params:
    taxon key (int): The taxon number used by GBIF for the specific rank (e.g. 1674437)
    limit (int): The number of images to randomly select from (default is 100000)
    
    Returns:
    tuple: A tuple of the form (species_name, image_url)"""

    # Base URL for GBIF occurrence search API
    base_url = 'https://api.gbif.org/v1/occurrence/search'

    # Query parameters
    params = {
        'mediaType': 'StillImage',
        'taxonKey': taxon_key,  # Change to your species name
        'limit': limit
    }

    try:
        # Make the request
        response = requests.get(base_url, params=params)
        data = response.json()

        results = []

        # Extract image URLs
        id = 1
        if 'results' in data:
            for occurrence in data['results']:
                if 'media' in occurrence:
                    for media in occurrence['media']:
                        scientific_name = occurrence.get('species', 'Unidentified species')
                        image_url = media.get('identifier')
                        if image_url and image_url.startswith("http"):
                            results.append((scientific_name, image_url))

                        if results and len(results) >= limit:
                            return random.choice(results)
        if results and len(results)>0:
            return random.choice(results)
        return ("", "")
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []

def request_images(taxon_key, image_number=10):
    """
    Fetches images for a given taxon key from the GBIF API
    
    Params:
    taxon key (int): The taxon number used by GBIF for the specific rank (e.g. 1674437)
    image_number (int): The number of image tuples to return (default is 10)
    
    Returns:
    list: A list of tuples of the form (species_name, image_url)"""

    print("in here")
    # Base URL for GBIF occurrence search API
    base_url = 'https://api.gbif.org/v1/occurrence/search'

    # Query parameters
    params = {
        'mediaType': 'StillImage',
        'taxonKey': taxon_key,  # Change to your species name
        'limit': image_number
    }

    try:
        # Make the request
        response = requests.get(base_url, params=params)
        data = response.json()

        results = []

        # Extract image URLs
        if 'results' in data:
            for occurrence in data['results']:
                if 'media' in occurrence:
                    for media in occurrence['media']:
                        scientific_name = occurrence.get('species', 'Unidentified species')
                        image_url = media.get('identifier')
                        if image_url and image_url.startswith("http") and not image_url == '':
                            results.append((scientific_name, image_url))
                        if len(results) >= image_number:
                            return results

        return results
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []

def save_image (image_info):
    """
    Downloads and saves the image from the provided URL into the 'images' directory.
    
    Params:
    image_info (tuple): A tuple containing the scientific name and image URL.
    """
    scientific_name = image_info[0]
    image_url = image_info [1]
    print(image_url)

    # Create an "images" directory if it doesn't exist
    os.makedirs('images', exist_ok=True)
    
    # Get the image content
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # Check for errors in the response
        
        # Format the image filename based on the scientific name and index
        image_filename = f"images/{scientific_name.replace(' ', '_')}.jpg"
        
        # Save the image
        with open(image_filename, 'wb') as img_file:
            img_file.write(response.content)
        
        print(f"Image saved: {image_filename}")
    
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {image_url}: {e}")

def label_image(species_name, image_path, image_label):
    directory, filename = os.path.split(image_path)
    name, extension = os.path.splitext(filename)

    # Remove any existing occurrence of the label type to avoid duplicates
    name = re.sub(rf"(_{image_label}|_{image_label}_\d+)", "", name)

    # Construct the new filename with the label appended
    new_filename = f"{name}_{image_label}{extension}"
    new_path = os.path.join(directory, new_filename)

    # Check if a file with the same name exists and increment if necessary
    counter = 1
    while os.path.exists(new_path):
        new_filename = f"{name}_{image_label}_{counter}{extension}"
        new_path = os.path.join(directory, new_filename)
        counter += 1

    # Rename or duplicate the image with the new filename
    os.rename(image_path, new_path)  # Or `shutil.copy` if you want to keep the original
    print(f"Image saved as: {new_path}")
    return new_path  # Return the new path for consistent reference
