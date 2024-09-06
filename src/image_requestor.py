import requests

def request_images(taxon_key, image_number=10):
    """
    Fetches images for a given species name from the GBIF API
    
    Params:
    species_name (str): The scientific name of the species (e.g. Dissosteira carolina (Linnaeus, 1758))
    image_number (int): The number of image URLs to return (default is 10)
    
    Returns:
    list: A list of image URLs"""

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

        image_urls = []

        # Extract image URLs
        if 'results' in data:
            for occurrence in data['results']:
                if 'media' in occurrence:
                    for media in occurrence['media']:
                        print(media)
                        image_urls.append(media['identifier'])
                        if len(image_urls) >= image_number:
                            return image_urls
        
        return image_urls
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []