from pygbif import species

def species_in_family (family_name, limit=10, status="accepted"):

    # Search for the family in GBIF to get the usageKey
    family_search = species.name_backbone(name=family_name, rank='family')

    # Get the family key (an identifier used by GBIF)
    family_key = family_search['usageKey']

    # Retrieve species under the family using the family key
    species_list = species.name_lookup(higherTaxonKey=family_key, rank='species', limit=20, status = status)

    return species_list['results']

# Define the family name
family_name = "Acrididae"

species_list = species_in_family(family_name, 10, "accepted")

# Print the species names
for result in species_list:
    print(result['scientificName'])