from pygbif import species

def sibling_families (family_name, rank="order", limit=20, status="accepted"):
    family_search = species.name_backbone(name=family_name, rank='family')

    order_key = family_search.get(rank+'Key')

    siblings = species.name_lookup(higherTaxonKey=order_key, rank='family', limit=limit)

    # Filter out the original family from the results
    sibling_families_list = [
        result for result in siblings['results'] 
        if result['scientificName'] != family_name
    ]

    return sibling_families_list

# Define the family name
family_name = "Acrididae"

siblings = sibling_families(family_name)

print("Sibling families in the same order:")
for sibling in siblings:
    print(sibling['scientificName'])