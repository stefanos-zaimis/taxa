from pygbif import species

def species_in_family (family_name, limit=10, status="accepted"):

    # Search for the family in GBIF to get the usageKey
    family_search = species.name_backbone(name=family_name, rank='family')

    # Get the family key (an identifier used by GBIF)
    family_key = family_search['usageKey']

    # Retrieve species under the family using the family key
    species_list = species.name_lookup(higherTaxonKey=family_key, rank='species', limit=20, status = status)

    return species_list

# Define the family name
family_name = "Staphylinidae"

species_list = species_in_family(family_name)

print("Total size:", len(species_list['results']))

# Print the species names
for species in species_list['results']:
    print(species['scientificName'], end="s")
    usage_key = species['key']
    print("Usage key: ", usage_key)