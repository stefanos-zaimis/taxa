from pygbif import species

def families_in_class(class_name="insecta", limit=100000, status="accepted"):
    # Search for the family in GBIF to get the usageKey
    class_search = species.name_backbone(name=class_name, rank='class')

    # Get the family key (an identifier used by GBIF)
    class_key = class_search['usageKey']

    # Retrieve species under the family using the family key
    class_list = species.name_lookup(higherTaxonKey=class_key, rank='family', limit=limit, status=status)

    return class_list['results']

# Define the class name
class_name = "Insecta"

# Get the family list with a limit of 150 families
family_list = families_in_class(class_name)

# Print the total size of the family list
print("Total size:", len(family_list))

# Print the family names
for family in family_list:
    print(family['scientificName'])