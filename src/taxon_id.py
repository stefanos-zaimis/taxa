import requests
from dataclasses import dataclass, asdict 
from typing import List, Optional
from enum import Enum

@dataclass
class TaxonFilter:
    dataset_key: int = 3
    taxon_id: Optional[int] = None
    q: Optional[str] = None
    name: Optional[str] = None
    scientific_name: Optional[str] = None
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
SEARCH_ENDPOINT = "nameusage/search"

def get_taxon_id():
    return