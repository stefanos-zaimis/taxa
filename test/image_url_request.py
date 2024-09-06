import requests

# Define the species and base URL
base_url = 'https://api.gbif.org/v1/occurrence/search'
params = {
    'mediaType': 'StillImage',
    'scientificName': 'Dissosteira carolina (Linnaeus, 1758)',  # Change to your species name
    'limit': 100
}

# Make the request
response = requests.get(base_url, params=params)
data = response.json()

# Extract and print image URLs
if 'results' in data:
    for occurrence in data['results']:
        if 'media' in occurrence:
            for media in occurrence['media']:
                print(f"Image URL: {media['identifier']}")
