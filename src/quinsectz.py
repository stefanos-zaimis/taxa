import asyncio

import aiohttp
from pygbif import species


def families_in_class(class_name="insecta", limit=100000, status="accepted"):
    # Search for the family in GBIF to get the usageKey
    class_search = species.name_backbone(name=class_name, rank="class")

    # Get the family key (an identifier used by GBIF)
    class_key = class_search["usageKey"]

    # Retrieve species under the family using the family key
    class_list = species.name_lookup(
        higherTaxonKey=class_key, rank="family", limit=limit, status=status
    )

    return class_list["results"]


def families_in_taxon(name="insecta", rank="class", limit=100000, status="accepted"):
    # Search for the family in GBIF to get the usageKey
    order_search = species.name_backbone(name=name, rank=rank)

    # Get the family key (an identifier used by GBIF)
    order_key = order_search["usageKey"]

    # Retrieve species under the family using the family key
    order_list = species.name_lookup(
        higherTaxonKey=order_key, rank="family", limit=limit, status=status
    )

    return order_list["results"]


def species_in_family(family_name, limit=100000, status="accepted"):

    # Search for the family in GBIF to get the usageKey
    family_search = species.name_backbone(name=family_name, rank="family")

    # Get the family key (an identifier used by GBIF)
    family_key = family_search["usageKey"]

    # Retrieve species under the family using the family key
    species_list = species.name_lookup(
        higherTaxonKey=family_key, rank="species", limit=limit, status=status
    )

    return species_list["results"]


def species_in_family_paginated(family_name, limit=100000, status="accepted"):

    # Search for the family in GBIF to get the usageKey
    family_search = species.name_backbone(name=family_name, rank="family")

    # Get the family key (an identifier used by GBIF)
    family_key = family_search["usageKey"]

    species_list = []
    offset = 0
    batch_size = 1000  # Maximum allowed by GBIF
    retrieved_count = 0

    while retrieved_count < limit:
        current_limit = min(batch_size, limit - retrieved_count)

        response = species.name_lookup(
            higherTaxonKey=family_key,
            rank="species",
            limit=current_limit,
            offset=offset,
            status=status,
        )

        species_list.extend(response["results"])

        retrieved_count += len(response["results"])
        offset += len(response["results"])

        if len(response["results"]) == 0:
            break

    return species_list


async def fetch_species_page(session, family_key, offset, limit, status):
    url = "https://api.gbif.org/v1/species/search"
    params = {
        "higherTaxonKey": family_key,
        "rank": "species",
        "limit": limit,
        "offset": offset,
        "status": status,
    }
    async with session.get(url, params=params) as response:
        result = await response.json()
        return result["results"]


async def species_in_family_paginated_concurrent(
    family_name, limit=100000, status="accepted"
):
    # Search for the family in GBIF to get the usageKey
    family_search = species.name_backbone(name=family_name, rank="family")

    # Get the family key (an identifier used by GBIF)
    family_key = family_search["usageKey"]

    species_list = []
    batch_size = 1000  # Maximum allowed by GBIF
    tasks = []

    async with aiohttp.ClientSession() as session:
        # Calculate the num of pages needed
        num_pages = (limit // batch_size) + (1 if limit % batch_size != 0 else 0)

        # Create asynchronous tasks for each batch/page
        for page in range(num_pages):
            offset = page * batch_size
            current_limit = min(batch_size, limit - offset)
            task = fetch_species_page(
                session, family_key, offset, current_limit, status
            )
            tasks.append(task)

        # Gather all results concurrently
        results = await asyncio.gather(*tasks)

    # Extend species list with results from all pages
    for result in results:
        species_list.extend(result)

    return species_list


def genus_in_family(family_name, limit=100000, status="accepted"):

    # Search for the family in GBIF to get the usageKey
    family_search = species.name_backbone(name=family_name, rank="family")

    # Get the family key (an identifier used by GBIF)
    family_key = family_search["usageKey"]

    # Retrieve species under the family using the family key
    genus_list = species.name_lookup(
        higherTaxonKey=family_key, rank="genus", limit=limit, status=status
    )

    return genus_list["results"]


def sibling_families(family_name, parent_rank="order", limit=100000, status="accepted"):
    family_search = species.name_backbone(name=family_name, rank="family")

    order_key = family_search.get(parent_rank + "Key")

    siblings = species.name_lookup(
        higherTaxonKey=order_key, rank="family", limit=limit + 1, status=status
    )

    # Filter out the original family from the results
    sibling_families_list = [
        result
        for result in siblings["results"]
        if result["scientificName"] != family_name
    ]

    # Ensure the result list has exactly `limit` entries
    if len(sibling_families_list) > limit:
        sibling_families_list = sibling_families_list[:limit]

    return sibling_families_list

