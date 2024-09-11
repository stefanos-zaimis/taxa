import requests
from dataclasses import dataclass, asdict 
from typing import List, Optional

@dataclass
class TaxonFilter:
    key: int = 3 # the dataset key
    id: Optional[str] = None # optional taxon id within said dataset
    q: Optional[str] = None
    name: Optional[str] = None
    scientificName: Optional[str] = None
    authorship: Optional[str] = None
    code: Optional[str] = None
    rank: Optional[str] = None
    status: Optional[str] = None
    verbose: Optional[bool] = None
    superkingdom: Optional[str] = None
    kingdom: Optional[str] = None
    subkingdom: Optional[str] = None
    superphylum: Optional[str] = None
    phylum: Optional[str] = None
    subphylum: Optional[str] = None
    superclass: Optional[str] = None
    taxon_class: Optional[str] = None
    subclass: Optional[str] = None
    superorder: Optional[str] = None
    order: Optional[str] = None
    suborder: Optional[str] = None
    superfamily: Optional[str] = None
    family: Optional[str] = None
    subfamily: Optional[str] = None
    tribe: Optional[str] = None
    subtribe: Optional[str] = None
    genus: Optional[str] = None
    subgenus: Optional[str] = None
    section: Optional[str] = None
    species: Optional[str] = None


BASE_URL = "https://api.checklistbank.org/"
SEARCH_ENDPOINT = "dataset/{key}/match/nameusage"

def get_exact_taxon_id(search_filters):
    url = BASE_URL+SEARCH_ENDPOINT.format(key=search_filters["key"])

    response = requests.get(url, params=search_filters)

    if response.status_code != 200:
        print(f"Error: {response.status_code} for URL: {response.url}")
        return None

    try:
        return response.json()
    except:
        print("Error: The file could not be parsed properly. Maybe it's not JSON?")
        return None

search_filters = TaxonFilter(
    key=3,
    scientificName="Insecta"
)
print(get_exact_taxon_id(search_filters=asdict(search_filters)))