import random

import image_scraper as img
import quinsectz as qi

# Define the class name
class_name = "Insecta"

# Get the family list
family_list = qi.families_in_class(class_name)

# Select random family
random_family = random.choice(family_list)

# Print the randomly selected family's name
    print("Randomly selected family:", random_family['scientificName'])

#Get Image
usage_key = random_family['key']
print("Taxon key:",usage_key)
url = "https://www.gbif.org/occurrence/gallery?taxon_key=" + str(usage_key) + "&occurrence_status=present"
img.scrape_random_species_text_dynamic(url)
