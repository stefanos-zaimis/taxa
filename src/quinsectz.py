from pygbif import species

def families_in_class(class_name="insecta", limit=100000, status="accepted"):
    # Search for the family in GBIF to get the usageKey
    class_search = species.name_backbone(name=class_name, rank='class')

    # Get the family key (an identifier used by GBIF)
    class_key = class_search['usageKey']

    # Retrieve species under the family using the family key
    class_list = species.name_lookup(higherTaxonKey=class_key, rank='family', limit=limit, status=status)

    return class_list['results']

def species_in_family(family_name, limit=100000, status="accepted"):

    # Search for the family in GBIF to get the usageKey
    family_search = species.name_backbone(name=family_name, rank='family')

    # Get the family key (an identifier used by GBIF)
    family_key = family_search['usageKey']

    # Retrieve species under the family using the family key
    species_list = species.name_lookup(higherTaxonKey=family_key, rank='species', limit=limit, status=status)

    return species_list['results']

def species_in_family_paginated(family_name, limit=100000, status="accepted"):

    # Search for the family in GBIF to get the usageKey
    family_search = species.name_backbone(name=family_name, rank='family')

    # Get the family key (an identifier used by GBIF)
    family_key = family_search['usageKey']

    species_list = []
    offset = 0
    batch_size = 1000 # Maximum allowed by GBIF
    retrieved_count = 0

    while retrieved_count < limit:
        current_limit = min(batch_size, limit - retrieved_count)

        response = species.name_lookup(higherTaxonKey=family_key, rank='species', limit=current_limit, offset=offset, status=status)

        species_list.extend(response['results'])

        retrieved_count += len(response['results'])
        offset += len(response['results'])

        if len(response['results']) == 0:
            break

    return species_list

def genus_in_family(family_name, limit=100000, status="accepted"):

    # Search for the family in GBIF to get the usageKey
    family_search = species.name_backbone(name=family_name, rank='family')

    # Get the family key (an identifier used by GBIF)
    family_key = family_search['usageKey']

    # Retrieve species under the family using the family key
    genus_list = species.name_lookup(higherTaxonKey=family_key, rank='genus', limit=limit, status=status)

    return genus_list['results']

def sibling_families(family_name, parent_rank="order", limit=100000, status="accepted"):
    family_search = species.name_backbone(name=family_name, rank='family')

    order_key = family_search.get(parent_rank+'Key')

    siblings = species.name_lookup(higherTaxonKey=order_key, rank='family', limit=limit+1, status=status)

    # Filter out the original family from the results
    sibling_families_list = [
        result for result in siblings['results'] 
        if result['scientificName'] != family_name
    ]

    # Ensure the result list has exactly `limit` entries
    if len(sibling_families_list) > limit:
        sibling_families_list = sibling_families_list[:limit]

    return sibling_families_list